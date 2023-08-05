import math
from typing import *

import torch
from torch import Tensor, nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .sequence import PositionalEncoding
from .utils import MeanMaxPooling


class ContextHead(nn.Module):
    """
    Args:
        deep_dims: size of the dictionary of embeddings.
        item_embedding: item embedding shared with sequence transformer.
        deep_embed_dims: the size of each embedding vector, can be either int or list of int.
        num_wide: the number of wide input features (default=0).
        num_shared: the number of embedding shared with sequence transformer (default=1).
        shared_embeddings_weight: list of embedding shared with candidate generation model.
    """
    def __init__(self, deep_dims, item_embedding, deep_embed_dims=100, num_wide=0,
                 num_shared=1, shared_embeddings_weight=None):
        super().__init__()
        if isinstance(deep_embed_dims, int):
            if shared_embeddings_weight is None:
                self.deep_embedding = nn.ModuleList([
                    nn.Embedding(deep_dim, deep_embed_dims)
                    for deep_dim in deep_dims
                ])
            else:
                self.deep_embedding = nn.ModuleList([
                    nn.Embedding(deep_dim, deep_embed_dims)
                    for deep_dim in deep_dims[:-len(shared_embeddings_weight)]
                ])
                from_pretrained = nn.ModuleList([
                     nn.Embedding.from_pretrained(shared_embedding_weight, freeze=True)
                    for shared_embedding_weight in shared_embeddings_weight
                ])
                self.deep_embedding.extend(from_pretrained)
        elif isinstance(deep_embed_dims, list) or isinstance(deep_embed_dims, tuple):
            self.deep_embedding = nn.ModuleList([
                nn.Embedding(deep_dim, deep_embed_dim)
                for deep_dim, deep_embed_dim in zip(deep_dims, deep_embed_dims)
            ])
        else:
            raise NotImplementedError()

        self.ctx_pe = False
        self.wide_layer_norm = nn.LayerNorm(num_wide)
        self.deep_embed_dims = deep_embed_dims
        self.shared_embed = nn.ModuleList([
                 item_embedding
                for _ in range(num_shared)
        ])
        
    def forward(self, deep_in:List[Tensor], wide_in:List[Tensor]=None, shared_in:List[Tensor]=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
        
        Return: 
            ctx_out: Tensor, shape [batch_size, len(deep_dims)*deep_embed_dims+(num_shared*seq_embed_dim)+num_wide]
        """
        deep_embedding_list = [self.deep_embedding[i](input_deep).unsqueeze(1)
                               for i, input_deep in enumerate(deep_in)]
        if shared_in is not None:
            shared_in_list = [self.shared_embed[i](input_shared).unsqueeze(1)
                              for i, input_shared in enumerate(shared_in)] 
            deep_embedding_list.extend(shared_in_list)
        ctx_out = torch.cat(deep_embedding_list, dim=2).squeeze(1)
        if wide_in is not None:
            wide_in_list = [wide_i.float() for wide_i in wide_in]
            wide_cat = torch.stack(wide_in_list, dim=0)
            wide_out = torch.transpose(wide_cat, dim1=1, dim0=0)
            wide_out_norm = self.wide_layer_norm(wide_out)
            ctx_out = torch.cat((ctx_out, wide_out_norm), dim=1)

        return ctx_out


class ContextTransformer(nn.Module):
    """
    [[B, ] * C] -> [B, cross_size]
    """
    def __init__(self, ctx_nums, cross_size, ctx_embed_size=100, ctx_num_heads=2,
                 ctx_hidden_size=512, ctx_num_layers=1, ctx_transformer_dropout=0.0,
                 ctx_pooling_dropout=0.0, ctx_pe=False):
        super().__init__()
        self.ctx_embedding = nn.ModuleList([
            nn.Embedding(ctx_num, ctx_embed_size)
            for ctx_num in ctx_nums
        ])
        self.ctx_pe = ctx_pe
        self.ctx_embed_size = ctx_embed_size
        if ctx_pe:
            self.pos_encoder = PositionalEncoding(d_model=ctx_embed_size,
                                                  dropout=ctx_transformer_dropout,
                                                  max_len=len(ctx_nums))
        encoder_layers = TransformerEncoderLayer(d_model=ctx_embed_size,
                                                 nhead=ctx_num_heads,
                                                 dropout=ctx_transformer_dropout,
                                                 dim_feedforward=ctx_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.ctx_encoder = TransformerEncoder(encoder_layers, num_layers=ctx_num_layers)
        self.ctx_pooling_dp = MeanMaxPooling(dropout=ctx_pooling_dropout)
        self.ctx_dense = torch.nn.Linear(in_features=2 * ctx_embed_size, out_features=cross_size)

    def forward(self, ctx_in):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :return: Tensor, shape [batch_size, cross_size]
        """
        # [[B, ] * C]
        ctx_embedding_list = [self.ctx_embedding[i](input_ctx).unsqueeze(1)
                                  for i, input_ctx in enumerate(ctx_in)]  # -> [(B, 1, E) * C]
        ctx_out = torch.cat(ctx_embedding_list, dim=1)  # -> (B, C, E)
        if self.ctx_pe:
            ctx_out = ctx_out * math.sqrt(self.ctx_embed_size)
            ctx_out = self.pos_encoder(ctx_out)
        ctx_out = self.ctx_encoder(ctx_out)  # -> (B, C, E)
        ctx_out = self.ctx_pooling_dp(ctx_out)  # -> (B, 2*E)
        ctx_out = self.ctx_dense(ctx_out)  # -> (B, cross_size)
        # print(ctx_out.shape)
        return ctx_out
