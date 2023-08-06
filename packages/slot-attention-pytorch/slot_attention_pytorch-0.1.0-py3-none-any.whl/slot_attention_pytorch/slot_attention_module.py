from math import sqrt

import torch
from torch import nn


class SlotAttentionModule(nn.Module):

    def __init__(self, num_slots: int, channels_enc: int, latent_size: int, attention_iters: float = 3,
                 eps: float = 1e-8,
                 mlp_size: int = 128) -> None:
        super().__init__()
        self.num_slots = num_slots
        self.attention_iters = attention_iters
        self.eps = eps
        self.scale = latent_size ** -0.5
        self.latent_size = latent_size
        self.mlp_size = mlp_size

        self.slots_mu = nn.Parameter(torch.rand(1, 1, latent_size))
        self.slots_log_sigma = nn.Parameter(torch.randn(1, 1, latent_size))
        with torch.no_grad():
            limit = sqrt(6.0 / (1 + latent_size))
            torch.nn.init.uniform_(self.slots_mu, -limit, limit)
            torch.nn.init.uniform_(self.slots_log_sigma, -limit, limit)
        self.to_q = nn.Linear(latent_size, latent_size, bias=False)
        self.to_k = nn.Linear(channels_enc, latent_size, bias=False)
        self.to_v = nn.Linear(channels_enc, latent_size, bias=False)

        self.gru = nn.GRUCell(latent_size, latent_size)

        mlp_size = max(latent_size, mlp_size)

        self.mlp = nn.Sequential(
            nn.Linear(latent_size, mlp_size),
            nn.ReLU(inplace=True),
            nn.Linear(mlp_size, latent_size)
        )

        self.norm_input = nn.LayerNorm(channels_enc, eps=0.001)
        self.norm_slots = nn.LayerNorm(latent_size, eps=0.001)
        self.norm_pre_ff = nn.LayerNorm(latent_size, eps=0.001)

    def forward(self, inputs: torch.Tensor, num_slots: None = None) -> torch.Tensor:
        b, n, _ = inputs.shape
        n_s = num_slots if num_slots is not None else self.num_slots

        mu = self.slots_mu.expand(b, n_s, -1)
        sigma = self.slots_log_sigma.expand(b, n_s, -1).exp()
        slots = torch.normal(mu, sigma)

        inputs = self.norm_input(inputs)
        k, v = self.to_k(inputs), self.to_v(inputs)

        for _ in range(self.attention_iters):
            slots_prev = slots

            slots = self.norm_slots(slots)
            q = self.to_q(slots)

            dots = torch.einsum('bid,bjd->bij', q, k) * self.scale
            attn = dots.softmax(dim=1) + self.eps
            attn = attn / attn.sum(dim=-1, keepdim=True)

            updates = torch.einsum('bjd,bij->bid', v, attn)

            slots = self.gru(
                updates.reshape(-1, self.latent_size),
                slots_prev.reshape(-1, self.latent_size)
            )

            slots = slots.reshape(b, -1, self.latent_size)
            slots = slots + self.mlp(self.norm_pre_ff(slots))

        return slots
