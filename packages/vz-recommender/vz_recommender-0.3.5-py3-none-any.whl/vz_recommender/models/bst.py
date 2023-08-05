from typing import *

import torch
from torch import nn
from transformers import AutoModel

from .context import ContextHead
from .sequence import SequenceTransformerHistoryLite, SequenceTransformerAEP


class BSTBottom(nn.Module):
    """
    Args:
        deep_dims: size of the dictionary of embeddings.
        seq_dim: size of the dictionary of embeddings.
        seq_embed_dim: the number of expected features in the encoder/decoder inputs.
        deep_embed_dims: the size of each embedding vector, can be either int or list of int.
        seq_hidden_size: the dimension of the feedforward network model.
        num_wide: the number of wide input features (default=0).
        num_shared: the number of embedding shared with sequence transformer (default=1).
    """
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__()
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, seq_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=True)
        
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = SequenceTransformerHistoryLite(
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.dense1 = torch.nn.Linear(
            in_features=nlp_dim+len(deep_dims)*deep_embed_dims+num_wide+seq_embed_dim+seq_embed_dim+(num_shared*seq_embed_dim),
            out_features=2 * seq_embed_dim)
        self.act1 = self.act2 = nn.LeakyReLU(0.2)
        self.dense2 = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_in: tensor, Tensor of shape [batch_size, 1] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
        """
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in, search_in=search_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)

        return outs


class BST(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_in: tensor, Tensor of shape [batch_size, 1] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in, search_in=search_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)


class BSTBERT(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, nlp_encoder_path, 
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_ids=None, att_mask=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(search_ids, att_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)


class BSTAudience(BSTBottom):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, nlp_encoder_path, 
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=True)
        
        self.sequence_transformer = SequenceTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.dense_out = torch.nn.Linear(seq_embed_dim, 1)
        self.act_out = nn.Sigmoid()

    def forward(self, deep_in, page_in, item_in, vl_in, wide_in=None, shared_in=None, search_ids=None, att_mask=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(search_ids, att_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense_out(user_out)
        outs = self.act_out(outs)
        return (outs, user_out)


class BSTCanGen(BSTBottom):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, nlp_encoder_path, 
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=True)
        
        self.sequence_transformer = SequenceTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, page_in, item_in, vl_in, wide_in=None, shared_in=None, search_ids=None, att_mask=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(search_ids, att_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)


class BSTBERTInference(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, nlp_encoder_path, 
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(**search_in).last_hidden_state[:,0,:].to(dtype=torch.float32)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)