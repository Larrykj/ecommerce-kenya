"""
Recommendation Service
Orchestrates all ML models and provides unified recommendation interface
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
from app.core.config import settings

# Optional ML imports
try:
    from app.ml.collaborative_filtering import CollaborativeFilteringEngine
    CF_AVAILABLE = True
except ImportError as e:
    CF_AVAILABLE = False
    print(f"[WARNING] Collaborative filtering not available: {e}")

try:
    from app.ml.matrix_factorization import MatrixFactorizationEngine
    MF_AVAILABLE = True
except ImportError as e:
    MF_AVAILABLE = False
    print(f"[WARNING] Matrix factorization not available: {e}")

try:
    from app.ml.hybrid_model import HybridRecommendationEngine
    HYBRID_AVAILABLE = True
except ImportError as e:
    HYBRID_AVAILABLE = False
    print(f"[WARNING] Hybrid model not available: {e}")


class RecommendationService:
    """
    Central recommendation service that coordinates all ML models
    """
    
    def __init__(self):
        # Initialize engines only if available
        self.cf_engine = CollaborativeFilteringEngine(
            n_neighbors=settings.KNN_NEIGHBORS
        ) if CF_AVAILABLE else None
        
        self.mf_engine = MatrixFactorizationEngine(
            n_factors=settings.SVD_FACTORS
        ) if MF_AVAILABLE else None
        
        self.hybrid_engine = HybridRecommendationEngine() if HYBRID_AVAILABLE else None
        
        self.models_trained = False
        self.last_training = None
        
        if not any([CF_AVAILABLE, MF_AVAILABLE, HYBRID_AVAILABLE]):
            print("[WARNING] No ML models available - using mock recommendations")
    
    async def train_models(
        self, 
        interactions: List[dict],
        products: List[dict]
    ):
        """
        Train all ML models
        
        Args:
            interactions: User-product interactions
            products: Product metadata
        """
        print("🤖 Training recommendation models...")
        
        # Prepare data
        cf_matrix = self.cf_engine.prepare_interaction_matrix(interactions)
        mf_matrix = self.mf_engine.prepare_data(interactions)
        
        # Train collaborative filtering
        self.cf_engine.train_user_based(cf_matrix)
        self.cf_engine.train_item_based(cf_matrix)
        print("✅ Collaborative filtering models trained")
        
        # Train matrix factorization
        self.mf_engine.train(mf_matrix)
        print("✅ Matrix factorization model trained")
        
        # Train hybrid model
        dataset, interactions_matrix, item_features = self.hybrid_engine.prepare_data(
            interactions, products
        )
        self.hybrid_engine.train(interactions_matrix, item_features)
        print("✅ Hybrid model trained")
        
        self.models_trained = True
        self.last_training = datetime.utcnow()
    
    async def get_personalized_recommendations(
        self,
        user_id: str,
        n_recommendations: int = 10,
        algorithm: str = "hybrid"
    ) -> List[Dict]:
        """
        Get personalized recommendations for a user
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of recommendations
            algorithm: Algorithm to use (user_based, item_based, hybrid, matrix_factorization)
            
        Returns:
            List of recommended products with scores
        """
        # Return mock recommendations if no models available
        if not any([CF_AVAILABLE, MF_AVAILABLE, HYBRID_AVAILABLE]):
            return self._get_mock_recommendations(user_id, n_recommendations)
        
        if not self.models_trained:
            return self._get_mock_recommendations(user_id, n_recommendations)
        
        try:
            if algorithm == "user_based" and self.cf_engine:
                recommendations = self.cf_engine.recommend_user_based(
                    user_id, n_recommendations
                )
            elif algorithm == "item_based" and self.cf_engine:
                recommendations = []
            elif algorithm == "matrix_factorization" and self.mf_engine:
                recommendations = self.mf_engine.recommend(
                    user_id, n_recommendations
                )
            elif algorithm == "hybrid" and self.hybrid_engine:
                recommendations = self.hybrid_engine.recommend(
                    user_id, n_recommendations
                )
            else:
                return self._get_mock_recommendations(user_id, n_recommendations)
            
            return [
                {"product_id": pid, "score": score, "algorithm": algorithm}
                for pid, score in recommendations
            ]
        
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return self._get_mock_recommendations(user_id, n_recommendations)
    
    def _get_mock_recommendations(self, user_id: str, n: int) -> List[Dict]:
        """Generate mock recommendations for testing"""
        return [
            {
                "product_id": f"mock_product_{i}",
                "score": 0.9 - (i * 0.1),
                "algorithm": "mock",
                "name": f"Sample Product {i+1}",
                "price": 1000 + (i * 500)
            }
            for i in range(min(n, 10))
        ]
    
    async def get_similar_products(
        self,
        product_id: str,
        n_similar: int = 10,
        algorithm: str = "item_based"
    ) -> List[Dict]:
        """
        Get products similar to a given product
        
        Args:
            product_id: Target product ID
            n_similar: Number of similar products
            algorithm: Algorithm to use
            
        Returns:
            List of similar products with similarity scores
        """
        if not any([CF_AVAILABLE, MF_AVAILABLE, HYBRID_AVAILABLE]):
            return self._get_mock_similar_products(product_id, n_similar)
            
        if not self.models_trained:
            return self._get_mock_similar_products(product_id, n_similar)
        
        try:
            if algorithm == "item_based" and self.cf_engine:
                similar_products = self.cf_engine.recommend_item_based(
                    product_id, n_similar
                )
            elif algorithm == "matrix_factorization" and self.mf_engine:
                similar_products = self.mf_engine.get_similar_items(
                    product_id, n_similar
                )
            elif algorithm == "hybrid" and self.hybrid_engine:
                similar_products = self.hybrid_engine.recommend_similar_items(
                    product_id, n_similar
                )
            else:
                return self._get_mock_similar_products(product_id, n_similar)
            
            return [
                {"product_id": pid, "similarity": score, "algorithm": algorithm}
                for pid, score in similar_products
            ]
        
        except Exception as e:
            print(f"Error finding similar products: {e}")
            return self._get_mock_similar_products(product_id, n_similar)
    
    def _get_mock_similar_products(self, product_id: str, n: int) -> List[Dict]:
        """Generate mock similar products for testing"""
        return [
            {
                "product_id": f"similar_{product_id}_{i}",
                "similarity": 0.95 - (i * 0.05),
                "algorithm": "mock",
                "name": f"Similar Product {i+1}"
            }
            for i in range(min(n, 10))
        ]
    
    async def get_frequently_bought_together(
        self,
        product_ids: List[str],
        n_recommendations: int = 5
    ) -> List[Dict]:
        """
        Get products frequently bought together
        
        Args:
            product_ids: List of product IDs in basket
            n_recommendations: Number of recommendations
            
        Returns:
            List of recommended bundle products
        """
        if not self.models_trained:
            return []
        
        try:
            recommendations = self.cf_engine.recommend_for_basket(
                product_ids, n_recommendations
            )
            
            return [
                {"product_id": pid, "score": score, "algorithm": "basket_analysis"}
                for pid, score in recommendations
            ]
        
        except Exception as e:
            print(f"Error finding bundle recommendations: {e}")
            return []
    
    async def get_trending_products(
        self,
        interactions: List[dict],
        time_window: str = "24h",
        county: Optional[str] = None,
        category: Optional[str] = None,
        n_items: int = 10
    ) -> List[Dict]:
        """
        Get trending products based on recent interactions
        
        Args:
            interactions: Recent interactions
            time_window: Time window (1h, 24h, 7d, 30d)
            county: Filter by county
            category: Filter by category
            n_items: Number of trending items
            
        Returns:
            List of trending products
        """
        # Parse time window
        time_deltas = {
            "1h": timedelta(hours=1),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30)
        }
        
        cutoff_time = datetime.utcnow() - time_deltas.get(time_window, timedelta(hours=24))
        
        # Filter interactions
        recent_interactions = [
            i for i in interactions
            if i.get('timestamp', datetime.utcnow()) >= cutoff_time
        ]
        
        if county:
            recent_interactions = [
                i for i in recent_interactions
                if i.get('county') == county
            ]
        
        # Count product occurrences with weights
        product_scores = {}
        weights = {
            'view': 1,
            'click': 2,
            'add_to_cart': 5,
            'purchase': 10,
            'wishlist': 3
        }
        
        for interaction in recent_interactions:
            pid = interaction['product_id']
            weight = weights.get(interaction['interaction_type'], 1)
            product_scores[pid] = product_scores.get(pid, 0) + weight
        
        # Sort by score
        trending = sorted(
            product_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_items]
        
        return [
            {"product_id": pid, "trending_score": score, "time_window": time_window}
            for pid, score in trending
        ]
    
    async def get_context_aware_recommendations(
        self,
        user_id: str,
        context: Dict,
        n_recommendations: int = 10
    ) -> List[Dict]:
        """
        Get context-aware recommendations based on time, location, season
        
        Args:
            user_id: Target user ID
            context: Context data (time_of_day, county, season, weather, etc.)
            n_recommendations: Number of recommendations
            
        Returns:
            List of context-aware recommendations
        """
        # Get base recommendations
        base_recs = await self.get_personalized_recommendations(
            user_id, n_recommendations * 2, "hybrid"
        )
        
        # Apply context filters and boost
        # This is a simplified version - in production, train separate models
        # or add context features to the hybrid model
        
        time_of_day = context.get('time_of_day')  # morning, afternoon, evening, night
        county = context.get('county')
        season = context.get('season')  # rainy, dry, festive
        
        # Context boost factors
        for rec in base_recs:
            boost = 1.0
            
            # Time-based boost (this would come from product metadata)
            # For now, simplified logic
            if time_of_day == "morning":
                boost *= 1.2  # Boost breakfast items, coffee, etc.
            elif time_of_day == "evening":
                boost *= 1.1  # Boost dinner items, entertainment
            
            # County-based boost
            if county:
                boost *= 1.3  # Boost local popular items
            
            # Season-based boost
            if season == "rainy":
                boost *= 1.2  # Boost raincoats, umbrellas
            elif season == "festive":
                boost *= 1.3  # Boost gifts, decorations
            
            rec['score'] *= boost
            rec['context_boost'] = boost
        
        # Re-sort and return top N
        sorted_recs = sorted(base_recs, key=lambda x: x['score'], reverse=True)
        return sorted_recs[:n_recommendations]
    
    def should_retrain(self) -> bool:
        """Check if models should be retrained"""
        if not self.models_trained:
            return True
        
        if self.last_training is None:
            return True
        
        time_since_training = datetime.utcnow() - self.last_training
        return time_since_training.total_seconds() > settings.MODEL_RETRAIN_INTERVAL
    
    async def save_models(self, base_path: str = "models"):
        """Save all trained models"""
        import os
        os.makedirs(base_path, exist_ok=True)
        
        self.cf_engine.save_model(f"{base_path}/collaborative_filtering.joblib")
        self.mf_engine.save_model(f"{base_path}/matrix_factorization.joblib")
        self.hybrid_engine.save_model(f"{base_path}/hybrid_model.joblib")
        print("✅ Models saved successfully")
    
    async def load_models(self, base_path: str = "models"):
        """Load trained models"""
        try:
            self.cf_engine.load_model(f"{base_path}/collaborative_filtering.joblib")
            self.mf_engine.load_model(f"{base_path}/matrix_factorization.joblib")
            self.hybrid_engine.load_model(f"{base_path}/hybrid_model.joblib")
            self.models_trained = True
            self.last_training = self.hybrid_engine.trained_at
            print("✅ Models loaded successfully")
        except Exception as e:
            print(f"[WARNING] Could not load models: {e}")
            self.models_trained = False


# Global instance
recommendation_service = RecommendationService()

