"""
Matrix Factorization for Recommendations
Implements SVD (Singular Value Decomposition) for latent feature extraction
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from typing import List, Tuple, Optional
import joblib
from datetime import datetime


class MatrixFactorizationEngine:
    """
    Matrix Factorization using SVD
    Decomposes user-item matrix into latent factors
    """
    
    def __init__(self, n_factors: int = 50, random_state: int = 42):
        """
        Initialize matrix factorization engine
        
        Args:
            n_factors: Number of latent factors
            random_state: Random seed for reproducibility
        """
        self.n_factors = n_factors
        self.random_state = random_state
        self.model = None
        self.user_item_matrix = None
        self.user_ids = []
        self.product_ids = []
        self.user_features = None
        self.item_features = None
        self.trained_at = None
        
    def prepare_data(self, interactions: List[dict]) -> pd.DataFrame:
        """
        Prepare interaction matrix from raw data
        
        Args:
            interactions: List of interaction dictionaries
            
        Returns:
            User-item matrix DataFrame
        """
        df = pd.DataFrame(interactions)
        
        # Weight different interaction types
        interaction_weights = {
            'view': 1.0,
            'click': 1.5,
            'add_to_cart': 3.0,
            'wishlist': 2.5,
            'purchase': 5.0,
            'review': 4.0
        }
        
        df['weighted_rating'] = df.apply(
            lambda row: interaction_weights.get(row['interaction_type'], 1.0) * 
                       (row.get('rating', 3.0) / 3.0),
            axis=1
        )
        
        # Create user-item matrix
        user_item_matrix = df.pivot_table(
            index='user_id',
            columns='product_id',
            values='weighted_rating',
            aggfunc='mean',
            fill_value=0
        )
        
        return user_item_matrix
    
    def train(self, user_item_matrix: pd.DataFrame):
        """
        Train SVD model on user-item matrix
        
        Args:
            user_item_matrix: User-item interaction matrix
        """
        self.user_item_matrix = user_item_matrix
        self.user_ids = user_item_matrix.index.tolist()
        self.product_ids = user_item_matrix.columns.tolist()
        
        # Apply SVD
        n_components = min(
            self.n_factors,
            min(len(self.user_ids), len(self.product_ids)) - 1
        )
        
        self.model = TruncatedSVD(
            n_components=n_components,
            random_state=self.random_state
        )
        
        # Fit and transform
        self.user_features = self.model.fit_transform(user_item_matrix.values)
        self.item_features = self.model.components_.T
        
        self.trained_at = datetime.utcnow()
        
    def predict_rating(self, user_id: str, product_id: str) -> float:
        """
        Predict rating for a user-product pair
        
        Args:
            user_id: User ID
            product_id: Product ID
            
        Returns:
            Predicted rating
        """
        if user_id not in self.user_ids or product_id not in self.product_ids:
            return 0.0
        
        user_idx = self.user_ids.index(user_id)
        product_idx = self.product_ids.index(product_id)
        
        # Dot product of user and item latent features
        rating = np.dot(self.user_features[user_idx], self.item_features[product_idx])
        
        return float(rating)
    
    def recommend(
        self, 
        user_id: str, 
        n_recommendations: int = 10,
        exclude_interacted: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using matrix factorization
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of recommendations
            exclude_interacted: Exclude items user has already interacted with
            
        Returns:
            List of (product_id, predicted_rating) tuples
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        if user_id not in self.user_ids:
            return []
        
        user_idx = self.user_ids.index(user_id)
        
        # Calculate predicted ratings for all items
        predicted_ratings = np.dot(
            self.user_features[user_idx],
            self.item_features.T
        )
        
        # Exclude already interacted items if requested
        if exclude_interacted:
            user_interactions = self.user_item_matrix.iloc[user_idx]
            interacted_indices = np.where(user_interactions > 0)[0]
            predicted_ratings[interacted_indices] = -np.inf
        
        # Get top N recommendations
        top_indices = np.argsort(predicted_ratings)[::-1][:n_recommendations]
        recommendations = [
            (self.product_ids[idx], float(predicted_ratings[idx]))
            for idx in top_indices
            if predicted_ratings[idx] > 0
        ]
        
        return recommendations
    
    def get_similar_items(
        self, 
        product_id: str, 
        n_similar: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Find similar items based on latent features
        
        Args:
            product_id: Target product ID
            n_similar: Number of similar items to return
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if product_id not in self.product_ids:
            return []
        
        product_idx = self.product_ids.index(product_id)
        product_vector = self.item_features[product_idx].reshape(1, -1)
        
        # Calculate cosine similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(product_vector, self.item_features)[0]
        
        # Get top N similar items (excluding the item itself)
        similar_indices = np.argsort(similarities)[::-1][1:n_similar+1]
        similar_items = [
            (self.product_ids[idx], float(similarities[idx]))
            for idx in similar_indices
        ]
        
        return similar_items
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'user_item_matrix': self.user_item_matrix,
            'user_ids': self.user_ids,
            'product_ids': self.product_ids,
            'user_features': self.user_features,
            'item_features': self.item_features,
            'n_factors': self.n_factors,
            'trained_at': self.trained_at
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.user_item_matrix = model_data['user_item_matrix']
        self.user_ids = model_data['user_ids']
        self.product_ids = model_data['product_ids']
        self.user_features = model_data['user_features']
        self.item_features = model_data['item_features']
        self.n_factors = model_data['n_factors']
        self.trained_at = model_data['trained_at']

