# Importing required PyTorch libraries
import torch
import torch.nn as nn
import torch.nn.functional as F

# Class for Image Preprocessing
class ImagePreprocessor(nn.Module):
    def __init__(self, patch_size):
        super(ImagePreprocessor, self).__init__()
        self.patch_size = patch_size  # Size of each patch

    def forward(self, x):
        # Dynamically get the batch size and channel dimensions
        batch_size, channel, _, _ = x.size()

        # Using unfold to create patches
        x_p = x.unfold(2, self.patch_size, self.patch_size).unfold(3, self.patch_size, self.patch_size)

        # Reshape into the desired shape
        x_p = x_p.permute(0, 2, 3, 1, 4, 5).contiguous()
        x_p = x_p.view(batch_size, -1, self.patch_size * self.patch_size * channel)

        # Now x_p should have shape [batch_size, (Height * Width) / (patch_size * patch_size), (patch_size * patch_size * channel)]
        
        return x_p

# Class for Patch Embedding
class PatchEmbedding(nn.Module):
    def __init__(self, patch_dim, D):
        super(PatchEmbedding, self).__init__()
        self.D = D  # Dimension to project to
        self.linear = nn.Linear(patch_dim, D)  # Linear projection layer

    def forward(self, x_p):
        # Project patches to D dimensions
        x_emb = self.linear(x_p)
        return x_emb

# Class for adding a Class Token
class ClassToken(nn.Module):
    def __init__(self, D):
        super(ClassToken, self).__init__()
        self.class_token_embedding = nn.Parameter(torch.randn(1, 1, D))  # Learnable class token

    def forward(self, x_emb):
        # Prepend class token to patch embeddings
        batch_size = x_emb.size(0)
        class_token = self.class_token_embedding.repeat(batch_size, 1, 1)
        x_class = torch.cat([class_token, x_emb], dim=1)
        return x_class

# Class for Position Embeddings
class PositionEmbedding(nn.Module):
    def __init__(self, seq_len, D):
        super(PositionEmbedding, self).__init__()
        self.position_embeddings = nn.Parameter(torch.randn(1, seq_len, D))  # Learnable position embeddings

    def forward(self, x_class):
        # Add position embeddings
        x_pos = x_class + self.position_embeddings
        return x_pos

# Class for Transformer Encoder
class TransformerEncoder(nn.Module):
    def __init__(self, D, num_layers, num_heads, mlp_size):
        super(TransformerEncoder, self).__init__()
        self.num_layers = num_layers
        self.layer_norm = nn.LayerNorm(D)
        self.multihead_attention = nn.MultiheadAttention(D, num_heads=num_heads, batch_first=True)
        self.mlp = nn.Sequential(
            nn.Linear(D, mlp_size),
            nn.GELU(),
            nn.Linear(mlp_size, D)
        )

    def forward(self, x_pos):
        # Transformer Encoder Logic
        for _ in range(self.num_layers):
            x_norm = self.layer_norm(x_pos)
            x_att, _ = self.multihead_attention(x_norm, x_norm, x_norm)
            x_pos = x_pos + x_att
            x_pos = x_pos + self.mlp(self.layer_norm(x_pos))
        return x_pos

# Class for Classification Head
class ClassificationHead(nn.Module):
    def __init__(self, D, num_classes):
        super(ClassificationHead, self).__init__()
        self.linear = nn.Linear(D, num_classes)  # Linear layer for classification

    def forward(self, x_transformed):
        # Take the class token and perform classification
        x_class_token = x_transformed[:, 0, :]
        output = self.linear(x_class_token)
        return output

# Main Vision Transformer Class
class VisionTransformer(nn.Module):
    def __init__(self, patch_size, D, num_layers, num_classes, num_heads, mlp_size):
        super(VisionTransformer, self).__init__()
        self.image_preprocessor = ImagePreprocessor(patch_size)
        self.patch_embedding = PatchEmbedding(patch_size * patch_size * 3, D)  # 3 channels, patch_size x patch_size patches
        self.class_token = ClassToken(D)
        self.position_embedding = PositionEmbedding( ((224*224)//(patch_size*patch_size)) + 1 , D)  # 196 patches + 1 class token
        self.transformer_encoder = TransformerEncoder(D, num_layers, num_heads, mlp_size)
        self.classification_head = ClassificationHead(D, num_classes)

    def forward(self, x):
        # Preprocess the image into patches
        x_p = self.image_preprocessor(x)
    
        # Generate patch embeddings
        x_emb = self.patch_embedding(x_p)
    
        # Prepend the class token
        x_class = self.class_token(x_emb)
    
        # Add position embeddings
        x_pos = self.position_embedding(x_class)
    
        # Pass through the Transformer Encoder
        x_transformed = self.transformer_encoder(x_pos)
    
        # Perform classification
        output = self.classification_head(x_transformed)
    
        return output
