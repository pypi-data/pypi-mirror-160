import math
from typing import *

import torch
from torch import nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .utils import MeanMaxPooling


class PositionalEncoding(nn.Module):
    """
    [B, S, E] -> [B, S, E]
    """
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        """
        Constant layer of positional encoding

        :param d_model: int, dimension of token embedding
        :param max_len: int, max length of sequence
        :param dropout: float
        """
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        :param x: Tensor, shape [batch_size, seq_len, embedding_dim]
        :return: : Tensor, shape [batch_size, seq_len, embedding_dim]
        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class SequenceTransformerHistory(nn.Module):
    """
    Args:
        seq_num: size of the dictionary of embeddings.
        seq_embed_dim: the number of expected features in the encoder/decoder inputs (default=200).
        seq_max_length: the max sequence input length (default=8).
        seq_num_heads: the number of heads in the multiheadattention models (default=4).
        seq_hidden_size: the dimension of the feedforward network model (default=512).
        seq_transformer_dropout: the dropout value (default=0.0).
        seq_num_layers: the number of sub-encoder-layers in the encoder (default=2).
        seq_pooling_dropout: the dropout value (default=0.0).
        seq_pe: If "True" then positional encoding is applied
    """
    def __init__(self, seq_num, seq_embed_dim=200, seq_max_length=8, seq_num_heads=4, seq_hidden_size=512, seq_transformer_dropout=0.0, 
                 seq_num_layers=2, seq_pooling_dropout=0.0, seq_pe=True):
        super().__init__()
        self.seq_embedding = nn.Embedding(seq_num, seq_embed_dim)
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)

    @staticmethod
    def create_key_padding_mask(seq_in, valid_length):
        device = valid_length.device
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(valid_length.unsqueeze(1))
        return mask

    def forward(self, seq_in, vl_in, seq_history=None):
        """
        Args:
            seq_in: Tensor, shape [batch_size, seq_len]
            vl_in: Tensor, shape [batch_size]
            seq_history: Tensor, shape [batch_size, history_len]

        Return: 
            Tensor, shape [batch_size, 2*seq_embed_dim]
        """
        # print("initial_shape:",input_seq.shape)
        # (B, 5), (B, 10)
        seq_embed_out = self.seq_embedding(seq_in.long())
        # history_embed_out = self.seq_embedding(input_history_seq.long())
        # history_embed_out = history_embed_out.transpose(0, 1).mean(dim=0, keepdim=True)
        # combined_embed_out = torch.cat([history_embed_out, seq_embed_out], dim=0)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)

        return seq_out


class SequenceTransformerHistoryLite(SequenceTransformerHistory):
    def __init__(self, item_embedding, seq_embed_dim, seq_max_length=8, seq_num_heads=4,
                 seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True):
        super(SequenceTransformerHistory, self).__init__()
        self.seq_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)


class SequenceTransformerAEP(SequenceTransformerHistory):
    def __init__(self, page_embedding, item_embedding, seq_embed_dim, seq_max_length=8, seq_num_heads=4,
                 seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True):
        super(SequenceTransformerHistory, self).__init__()
        self.page_embedding = page_embedding
        self.item_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
    
    def forward(self, page_in, item_in, vl_in, seq_history=None):
        """
        Args:
            seq_in: Tensor, shape [batch_size, seq_len]
            vl_in: Tensor, shape [batch_size]
            seq_history: Tensor, shape [batch_size, history_len]

        Return: 
            Tensor, shape [batch_size, 2*seq_embed_dim]
        """
        # print("initial_shape:",input_seq.shape)
        # (B, 5), (B, 10)
        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())
        seq_embed_out = torch.add(page_embed_out, item_embed_out)

        # seq_embed_out = self.seq_embedding(seq_in.long())
        # history_embed_out = self.seq_embedding(input_history_seq.long())
        # history_embed_out = history_embed_out.transpose(0, 1).mean(dim=0, keepdim=True)
        # combined_embed_out = torch.cat([history_embed_out, seq_embed_out], dim=0)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=page_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)

        return seq_out




# class SequenceTransformerAEP(nn.Module):
#     """
#     Args:
#         seq_num: size of the dictionary of embeddings.
#         seq_embed_dim: the number of expected features in the encoder/decoder inputs (default=200).
#         seq_max_length: the max sequence input length (default=8).
#         seq_num_heads: the number of heads in the multiheadattention models (default=4).
#         seq_hidden_size: the dimension of the feedforward network model (default=512).
#         seq_transformer_dropout: the dropout value (default=0.0).
#         seq_num_layers: the number of sub-encoder-layers in the encoder (default=2).
#         seq_pooling_dropout: the dropout value (default=0.0).
#         seq_pe: If "True" then positional encoding is applied
#     """
#     def __init__(self, seq_num, seq_embed_dim=[200, 100], seq_max_length=8, seq_num_heads=4, 
#                  seq_hidden_size=512, seq_transformer_dropout=0.0, 
#                  seq_num_layers=2, seq_pooling_dropout=0.0, seq_pe=True):
#         super().__init__()
#         if isinstance(seq_num, list):
#             self.seq_embedding = nn.ModuleList([
#                 nn.Embedding(sn, se)
#                 for (sn, se) in map(None, seq_num, seq_embed_dim)
#             ])
#         else:
#             self.seq_embedding = nn.Embedding(seq_num, seq_embed_dim)
#         self.seq_pos = seq_pe
#         self.seq_embed_dim = seq_embed_dim
#         if seq_pe:
#             self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
#                                                   dropout=seq_transformer_dropout,
#                                                   max_len=seq_max_length)
#         encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
#                                                  nhead=seq_num_heads,
#                                                  dropout=seq_transformer_dropout,
#                                                  dim_feedforward=seq_hidden_size,
#                                                  activation='relu',
#                                                  batch_first=True)
#         self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
#         self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)

#     @staticmethod
#     def create_key_padding_mask(seq_in, valid_length):
#         device = valid_length.device
#         mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
#         mask = ~mask.lt(valid_length.unsqueeze(1))
#         return mask

#     def forward(self, seq_in, vl_in, seq_history=None):
#         """
#         Args:
#             seq_in: Tensor, shape [batch_size, seq_len]
#             vl_in: Tensor, shape [batch_size]
#             seq_history: Tensor, shape [batch_size, history_len]

#         Return: 
#             Tensor, shape [batch_size, 2*seq_embed_dim]
#         """
#         # print("initial_shape:",input_seq.shape)
#         # (B, 5), (B, 10)
#         seq_embed_out = self.seq_embedding(seq_in.long())
#         print(seq_embed_out)
#         print(seq_embed_out.size())
#         # history_embed_out = self.seq_embedding(input_history_seq.long())
#         # history_embed_out = history_embed_out.transpose(0, 1).mean(dim=0, keepdim=True)
#         # combined_embed_out = torch.cat([history_embed_out, seq_embed_out], dim=0)
#         seq_out = seq_embed_out
#         if self.seq_pos:
#             seq_out = seq_out * math.sqrt(self.seq_embed_dim)
#             seq_out = self.pos_encoder(seq_out)
#         mask = self.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
#         seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
#         if mask[:, 0].any():
#             seq_out = seq_out.nan_to_num(nan=0.0)
#         seq_out = self.seq_pooling_dp(seq_out)

#         return seq_out