"""
Collaborative Filtering Recommendation Engine
Implements User-Based and Item-Based Collaborative Filtering
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional
import joblib
from datetime import datetime


class CollaborativeFilteringEngine:
    """
    Collaborative Filtering Engine using KNN
    Supports both user-based and item-based filtering
    """
    
    def __init__(self, n_neighbors: int = 20, metric: str = 'cosine'):
        """
        Initialize the collaborative filtering engine
        
        Args:
            n_neighbors: Number of nearest neighbors to consider
            metric: Distance metric (cosine, euclidean, etc.)
        """
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.user_model = None
        self.item_model = None
        self.user_item_matrix = None
        self.user_ids = []
        self.product_ids = []
        self.trained_at = None
        
    def prepare_interaction_matrix(self, interactions: List[dict]) -> pd.DataFrame:
        """
        Prepare user-item interaction matrix from interaction data
        
        Args:
            interactions: List of interaction dictionaries
            
        Returns:
            User-item matrix DataFrame
        """
        df = pd.DataFrame(interactions)
        
        # Create ratings based on interaction types
        interaction_weights = {
            'view': 1.0,
            'click': 1.5,
            'add_to_cart': 3.0,
            'wishlist': 2.5,
            'purchase': 5.0,
            'review': 4.0
        }
        
        # Apply weights
        df['weighted_rating'] = df.apply(
            lambda row: interaction_weights.get(row['interaction_type'], 1.0) * 
                       (row.get('rating', 3.0) / 3.0),
            axis=1
        )
        
        # Create pivot table (user-item matrix)
        user_item_matrix = df.pivot_table(
            index='user_id',
            columns='product_id',
            values='weighted_rating',
            aggfunc='mean',
            fill_value=0
        )
        
        return user_item_matrix
    
    def train_user_based(self, user_item_matrix: pd.DataFrame):
        """
        Train user-based collaborative filtering model
        
        Args:
            user_item_matrix: User-item interaction matrix
        """
        self.user_item_matrix = user_item_matrix
        self.user_ids = user_item_matrix.index.tolist()
        self.product_ids = user_item_matrix.columns.tolist()
        
        # Train KNN model on user similarities
        self.user_model = NearestNeighbors(
            n_neighbors=min(self.n_neighbors, len(self.user_ids)),
            metric=self.metric,
            algorithm='brute'
        )
        self.user_model.fit(user_item_matrix.values)
        self.trained_at = datetime.utcnow()
        
    def train_item_based(self, user_item_matrix: pd.DataFrame):
        """
        Train item-based collaborative filtering model
        
        Args:
            user_item_matrix: User-item interaction matrix
        """
        self.user_item_matrix = user_item_matrix
        self.user_ids = user_item_matrix.index.tolist()
        self.product_ids = user_item_matrix.columns.tolist()
        
        # Train KNN model on item similarities
        self.item_model = NearestNeighbors(
            n_neighbors=min(self.n_neighbors, len(self.product_ids)),
            metric=self.metric,
            algorithm='brute'
        )
        self.item_model.fit(user_item_matrix.T.values)
        self.trained_at = datetime.utcnow()
    
    def recommend_user_based(
        self, 
        user_id: str, 
        n_recommendations: int = 10,
        exclude_interacted: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using user-based collaborative filtering
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of recommendations to generate
            exclude_interacted: Exclude items user has already interacted with
            
        Returns:
            List of (product_id, score) tuples
        """
        if self.user_model is None:
            raise ValueError("User-based model not trained. Call train_user_based first.")
        
        if user_id not in self.user_ids:
            return []
        
        # Get user index
        user_idx = self.user_ids.index(user_id)
        user_vector = self.user_item_matrix.iloc[user_idx].values.reshape(1, -1)
        
        # Find similar users
        distances, indices = self.user_model.kneighbors(user_vector)
        
        # Get items from similar users
        similar_user_indices = indices[0][1:]  # Exclude the user themselves
        similar_users_matrix = self.user_item_matrix.iloc[similar_user_indices]
        
        # Calculate weighted average of similar users' ratings
        similarities = 1 - distances[0][1:]  # Convert distance to similarity
        weighted_ratings = (similar_users_matrix.T * similarities).sum(axis=1) / similarities.sum()
        
        # Exclude already interacted items if requested
        if exclude_interacted:
            user_interactions = self.user_item_matrix.iloc[user_idx]
            weighted_ratings[user_interactions > 0] = -np.inf
        
        # Get top N recommendations
        top_indices = np.argsort(weighted_ratings.values)[::-1][:n_recommendations]
        recommendations = [
            (self.product_ids[idx], float(weighted_ratings.values[idx]))
            for idx in top_indices
            if weighted_ratings.values[idx] > 0
        ]
        
        return recommendations
    
    def recommend_item_based(
        self, 
        product_id: str, 
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using item-based collaborative filtering
        
        Args:
            product_id: Target product ID
            n_recommendations: Number of similar items to recommend
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if self.item_model is None:
            raise ValueError("Item-based model not trained. Call train_item_based first.")
        
        if product_id not in self.product_ids:
            return []
        
        # Get product index
        product_idx = self.product_ids.index(product_id)
        product_vector = self.user_item_matrix.T.iloc[product_idx].values.reshape(1, -1)
        
        # Find similar items
        distances, indices = self.item_model.kneighbors(product_vector)
        
        # Convert to similarity scores
        similar_items = [
            (self.product_ids[idx], float(1 - distances[0][i]))
            for i, idx in enumerate(indices[0][1:n_recommendations+1])
        ]
        
        return similar_items
    
    def recommend_for_basket(
        self, 
        product_ids: List[str], 
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Recommend items based on a basket of products (frequently bought together)
        
        Args:
            product_ids: List of product IDs in the basket
            n_recommendations: Number of recommendations
            
        Returns:
            List of (product_id, score) tuples
        """
        if self.item_model is None:
            raise ValueError("Item-based model not trained.")
        
        all_recommendations = {}
        
        # Get recommendations for each item in basket
        for pid in product_ids:
            if pid in self.product_ids:
                recs = self.recommend_item_based(pid, n_recommendations * 2)
                for rec_pid, score in recs:
                    if rec_pid not in product_ids:  # Exclude items already in basket
                        if rec_pid in all_recommendations:
                            all_recommendations[rec_pid] += score
                        else:
                            all_recommendations[rec_pid] = score
        
        # Sort by score and return top N
        sorted_recommendations = sorted(
            all_recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        return sorted_recommendations
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        model_data = {
            'user_model': self.user_model,
            'item_model': self.item_model,
            'user_item_matrix': self.user_item_matrix,
            'user_ids': self.user_ids,
            'product_ids': self.product_ids,
            'n_neighbors': self.n_neighbors,
            'metric': self.metric,
            'trained_at': self.trained_at
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        self.user_model = model_data['user_model']
        self.item_model = model_data['item_model']
        self.user_item_matrix = model_data['user_item_matrix']
        self.user_ids = model_data['user_ids']
        self.product_ids = model_data['product_ids']
        self.n_neighbors = model_data['n_neighbors']
        self.metric = model_data['metric']
        self.trained_at = model_data['trained_at']

