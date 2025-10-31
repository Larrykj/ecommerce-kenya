"""
Hybrid Recommendation Model using LightFM
Combines collaborative filtering with content-based features
"""
import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
from typing import List, Tuple, Optional, Dict
import joblib
from datetime import datetime
import pandas as pd


class HybridRecommendationEngine:
    """
    Hybrid recommendation engine using LightFM
    Combines user-item interactions with product metadata
    """
    
    def __init__(
        self, 
        loss: str = 'warp',
        learning_rate: float = 0.05,
        n_epochs: int = 30,
        n_components: int = 30,
        random_state: int = 42
    ):
        """
        Initialize hybrid model
        
        Args:
            loss: Loss function ('warp', 'bpr', 'logistic')
            learning_rate: Learning rate
            n_epochs: Number of training epochs
            n_components: Number of latent dimensions
            random_state: Random seed
        """
        self.loss = loss
        self.learning_rate = learning_rate
        self.n_epochs = n_epochs
        self.n_components = n_components
        self.random_state = random_state
        
        self.model = None
        self.dataset = None
        self.user_id_map = {}
        self.product_id_map = {}
        self.trained_at = None
        
    def prepare_data(
        self,
        interactions: List[dict],
        product_features: List[dict]
    ) -> Tuple[Dataset, any, any]:
        """
        Prepare data for LightFM training
        
        Args:
            interactions: List of user-product interactions
            product_features: List of product metadata
            
        Returns:
            Tuple of (dataset, interactions_matrix, item_features_matrix)
        """
        # Create dataset
        self.dataset = Dataset()
        
        # Get unique users and items
        user_ids = list(set(i['user_id'] for i in interactions))
        product_ids = list(set(i['product_id'] for i in interactions))
        
        # Extract product features
        all_features = set()
        for product in product_features:
            features = [
                f"category:{product.get('category', 'unknown')}",
                f"brand:{product.get('brand', 'unknown')}",
                f"price_range:{self._get_price_range(product.get('price', 0))}",
                f"rating:{int(product.get('average_rating', 0))}"
            ]
            all_features.update(features)
        
        # Fit dataset
        self.dataset.fit(
            users=user_ids,
            items=product_ids,
            item_features=list(all_features)
        )
        
        # Build interactions matrix
        interaction_data = [
            (i['user_id'], i['product_id'], self._get_interaction_weight(i))
            for i in interactions
        ]
        interactions_matrix, _ = self.dataset.build_interactions(interaction_data)
        
        # Build item features matrix
        product_feature_map = {}
        for product in product_features:
            pid = product['id']
            features = [
                f"category:{product.get('category', 'unknown')}",
                f"brand:{product.get('brand', 'unknown')}",
                f"price_range:{self._get_price_range(product.get('price', 0))}",
                f"rating:{int(product.get('average_rating', 0))}"
            ]
            product_feature_map[pid] = features
        
        item_features_data = [
            (pid, features)
            for pid, features in product_feature_map.items()
        ]
        item_features_matrix = self.dataset.build_item_features(item_features_data)
        
        # Store mappings
        self.user_id_map, _, self.product_id_map, _ = self.dataset.mapping()
        
        return self.dataset, interactions_matrix, item_features_matrix
    
    def _get_interaction_weight(self, interaction: dict) -> float:
        """Calculate weight for an interaction"""
        weights = {
            'view': 1.0,
            'click': 1.5,
            'add_to_cart': 3.0,
            'wishlist': 2.5,
            'purchase': 5.0,
            'review': 4.0
        }
        
        base_weight = weights.get(interaction['interaction_type'], 1.0)
        rating_multiplier = interaction.get('rating', 3.0) / 3.0
        
        return base_weight * rating_multiplier
    
    def _get_price_range(self, price: float) -> str:
        """Categorize price into ranges"""
        if price < 500:
            return "budget"
        elif price < 2000:
            return "mid"
        elif price < 10000:
            return "premium"
        else:
            return "luxury"
    
    def train(
        self,
        interactions_matrix: any,
        item_features_matrix: any = None
    ):
        """
        Train the hybrid model
        
        Args:
            interactions_matrix: User-item interactions
            item_features_matrix: Item features matrix
        """
        self.model = LightFM(
            loss=self.loss,
            learning_rate=self.learning_rate,
            no_components=self.n_components,
            random_state=self.random_state
        )
        
        self.model.fit(
            interactions_matrix,
            item_features=item_features_matrix,
            epochs=self.n_epochs,
            verbose=False
        )
        
        self.trained_at = datetime.utcnow()
    
    def recommend(
        self,
        user_id: str,
        n_recommendations: int = 10,
        item_features_matrix: any = None
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations for a user
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of recommendations
            item_features_matrix: Item features for scoring
            
        Returns:
            List of (product_id, score) tuples
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        if user_id not in self.user_id_map:
            return []
        
        user_idx = self.user_id_map[user_id]
        
        # Get all product indices
        n_items = len(self.product_id_map)
        
        # Predict scores for all items
        scores = self.model.predict(
            user_idx,
            np.arange(n_items),
            item_features=item_features_matrix
        )
        
        # Get top N recommendations
        top_indices = np.argsort(-scores)[:n_recommendations]
        
        # Map back to product IDs
        idx_to_product = {v: k for k, v in self.product_id_map.items()}
        recommendations = [
            (idx_to_product[idx], float(scores[idx]))
            for idx in top_indices
            if idx in idx_to_product
        ]
        
        return recommendations
    
    def recommend_similar_items(
        self,
        product_id: str,
        n_similar: int = 10,
        item_features_matrix: any = None
    ) -> List[Tuple[str, float]]:
        """
        Find similar items based on item representations
        
        Args:
            product_id: Target product ID
            n_similar: Number of similar items
            item_features_matrix: Item features
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if self.model is None or product_id not in self.product_id_map:
            return []
        
        product_idx = self.product_id_map[product_id]
        
        # Get item embeddings
        item_embeddings = self.model.item_embeddings
        target_embedding = item_embeddings[product_idx]
        
        # Calculate similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(
            target_embedding.reshape(1, -1),
            item_embeddings
        )[0]
        
        # Get top N similar items (excluding the item itself)
        top_indices = np.argsort(-similarities)[1:n_similar+1]
        
        idx_to_product = {v: k for k, v in self.product_id_map.items()}
        similar_items = [
            (idx_to_product[idx], float(similarities[idx]))
            for idx in top_indices
            if idx in idx_to_product
        ]
        
        return similar_items
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'dataset': self.dataset,
            'user_id_map': self.user_id_map,
            'product_id_map': self.product_id_map,
            'loss': self.loss,
            'learning_rate': self.learning_rate,
            'n_epochs': self.n_epochs,
            'n_components': self.n_components,
            'trained_at': self.trained_at
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.dataset = model_data['dataset']
        self.user_id_map = model_data['user_id_map']
        self.product_id_map = model_data['product_id_map']
        self.loss = model_data['loss']
        self.learning_rate = model_data['learning_rate']
        self.n_epochs = model_data['n_epochs']
        self.n_components = model_data['n_components']
        self.trained_at = model_data['trained_at']

