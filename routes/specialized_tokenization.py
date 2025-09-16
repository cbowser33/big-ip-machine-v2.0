"""
Specialized Tokenization Functions for Version 1.1
Each content category has its own optimized tokenization logic
"""

from typing import Dict, Any, List
import random
import time
import logging
from .tokenization_categories import (
    CONTENT_CATEGORIES, 
    get_category_tokenization_structure,
    get_category_by_file_extension
)

logger = logging.getLogger(__name__)

class SpecializedTokenizer:
    """Handles specialized tokenization for different content categories"""
    
    def __init__(self):
        self.total_tokens = 1000  # Standard token amount
    
    def tokenize_film(self, content_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized tokenization for film content"""
        logger.info(f"Applying film-specific tokenization for {content_id}")
        
        structure = get_category_tokenization_structure('film')
        originality_factor = analysis.get('originality_score', 90) / 100
        
        # Film-specific analysis factors
        film_factors = {
            'production_quality': random.uniform(0.8, 1.0),
            'narrative_complexity': random.uniform(0.7, 0.95),
            'technical_innovation': random.uniform(0.6, 0.9),
            'commercial_potential': random.uniform(0.5, 0.85)
        }
        
        tokenization = self._create_base_tokenization(content_id, 'film', analysis)
        
        for category, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            
            # Apply film-specific value adjustments
            value_multiplier = 1.0
            if 'cinematography' in category:
                value_multiplier *= film_factors['technical_innovation']
            elif 'narrative' in category:
                value_multiplier *= film_factors['narrative_complexity']
            elif 'distribution' in category:
                value_multiplier *= film_factors['commercial_potential']
            
            token_value = details['base_value'] * originality_factor * value_multiplier
            
            tokenization['token_categories'][category] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': round(value_multiplier, 3)
                }
            }
        
        # Add film-specific metadata
        tokenization['category_analysis'] = {
            'content_category': 'film',
            'production_quality_score': round(film_factors['production_quality'] * 100, 1),
            'narrative_complexity_score': round(film_factors['narrative_complexity'] * 100, 1),
            'technical_innovation_score': round(film_factors['technical_innovation'] * 100, 1),
            'commercial_potential_score': round(film_factors['commercial_potential'] * 100, 1)
        }
        
        return tokenization
    
    def tokenize_animation(self, content_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized tokenization for animation content"""
        logger.info(f"Applying animation-specific tokenization for {content_id}")
        
        structure = get_category_tokenization_structure('animation')
        originality_factor = analysis.get('originality_score', 90) / 100
        
        # Animation-specific analysis factors
        animation_factors = {
            'artistic_style': random.uniform(0.8, 1.0),
            'animation_quality': random.uniform(0.7, 0.95),
            'character_appeal': random.uniform(0.6, 0.9),
            'technical_complexity': random.uniform(0.5, 0.85)
        }
        
        tokenization = self._create_base_tokenization(content_id, 'animation', analysis)
        
        for category, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            
            # Apply animation-specific value adjustments
            value_multiplier = 1.0
            if 'artistry' in category:
                value_multiplier *= animation_factors['artistic_style']
            elif 'character' in category:
                value_multiplier *= animation_factors['character_appeal']
            elif 'technical' in category:
                value_multiplier *= animation_factors['technical_complexity']
            
            token_value = details['base_value'] * originality_factor * value_multiplier
            
            tokenization['token_categories'][category] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': round(value_multiplier, 3)
                }
            }
        
        tokenization['category_analysis'] = {
            'content_category': 'animation',
            'artistic_style_score': round(animation_factors['artistic_style'] * 100, 1),
            'animation_quality_score': round(animation_factors['animation_quality'] * 100, 1),
            'character_appeal_score': round(animation_factors['character_appeal'] * 100, 1),
            'technical_complexity_score': round(animation_factors['technical_complexity'] * 100, 1)
        }
        
        return tokenization
    
    def tokenize_screenplay(self, content_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized tokenization for screenplay content"""
        logger.info(f"Applying screenplay-specific tokenization for {content_id}")
        
        structure = get_category_tokenization_structure('screenplay')
        originality_factor = analysis.get('originality_score', 90) / 100
        
        # Screenplay-specific analysis factors
        screenplay_factors = {
            'dialogue_quality': random.uniform(0.8, 1.0),
            'plot_originality': random.uniform(0.7, 0.95),
            'character_depth': random.uniform(0.6, 0.9),
            'adaptation_potential': random.uniform(0.5, 0.85)
        }
        
        tokenization = self._create_base_tokenization(content_id, 'screenplay', analysis)
        
        for category, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            
            # Apply screenplay-specific value adjustments
            value_multiplier = 1.0
            if 'dialogue' in category:
                value_multiplier *= screenplay_factors['dialogue_quality']
            elif 'plot' in category:
                value_multiplier *= screenplay_factors['plot_originality']
            elif 'character' in category:
                value_multiplier *= screenplay_factors['character_depth']
            elif 'adaptation' in category:
                value_multiplier *= screenplay_factors['adaptation_potential']
            
            token_value = details['base_value'] * originality_factor * value_multiplier
            
            tokenization['token_categories'][category] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': round(value_multiplier, 3)
                }
            }
        
        tokenization['category_analysis'] = {
            'content_category': 'screenplay',
            'dialogue_quality_score': round(screenplay_factors['dialogue_quality'] * 100, 1),
            'plot_originality_score': round(screenplay_factors['plot_originality'] * 100, 1),
            'character_depth_score': round(screenplay_factors['character_depth'] * 100, 1),
            'adaptation_potential_score': round(screenplay_factors['adaptation_potential'] * 100, 1)
        }
        
        return tokenization
    
    def tokenize_book_writing(self, content_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized tokenization for book writing content"""
        logger.info(f"Applying book writing-specific tokenization for {content_id}")
        
        structure = get_category_tokenization_structure('book_writing')
        originality_factor = analysis.get('originality_score', 90) / 100
        
        # Book writing-specific analysis factors
        book_factors = {
            'prose_quality': random.uniform(0.8, 1.0),
            'narrative_innovation': random.uniform(0.7, 0.95),
            'world_building': random.uniform(0.6, 0.9),
            'market_appeal': random.uniform(0.5, 0.85)
        }
        
        tokenization = self._create_base_tokenization(content_id, 'book_writing', analysis)
        
        for category, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            
            # Apply book-specific value adjustments
            value_multiplier = 1.0
            if 'prose' in category:
                value_multiplier *= book_factors['prose_quality']
            elif 'plot' in category:
                value_multiplier *= book_factors['narrative_innovation']
            elif 'world' in category:
                value_multiplier *= book_factors['world_building']
            elif 'publishing' in category:
                value_multiplier *= book_factors['market_appeal']
            
            token_value = details['base_value'] * originality_factor * value_multiplier
            
            tokenization['token_categories'][category] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': round(value_multiplier, 3)
                }
            }
        
        tokenization['category_analysis'] = {
            'content_category': 'book_writing',
            'prose_quality_score': round(book_factors['prose_quality'] * 100, 1),
            'narrative_innovation_score': round(book_factors['narrative_innovation'] * 100, 1),
            'world_building_score': round(book_factors['world_building'] * 100, 1),
            'market_appeal_score': round(book_factors['market_appeal'] * 100, 1)
        }
        
        return tokenization
    
    def tokenize_digital_art(self, content_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized tokenization for digital art content"""
        logger.info(f"Applying digital art-specific tokenization for {content_id}")
        
        structure = get_category_tokenization_structure('digital_art')
        originality_factor = analysis.get('originality_score', 90) / 100
        
        # Digital art-specific analysis factors
        art_factors = {
            'artistic_skill': random.uniform(0.8, 1.0),
            'concept_originality': random.uniform(0.7, 0.95),
            'technical_execution': random.uniform(0.6, 0.9),
            'commercial_viability': random.uniform(0.5, 0.85)
        }
        
        tokenization = self._create_base_tokenization(content_id, 'digital_art', analysis)
        
        for category, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            
            # Apply art-specific value adjustments
            value_multiplier = 1.0
            if 'composition' in category:
                value_multiplier *= art_factors['artistic_skill']
            elif 'concept' in category:
                value_multiplier *= art_factors['concept_originality']
            elif 'technical' in category:
                value_multiplier *= art_factors['technical_execution']
            elif 'commercial' in category:
                value_multiplier *= art_factors['commercial_viability']
            
            token_value = details['base_value'] * originality_factor * value_multiplier
            
            tokenization['token_categories'][category] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': round(value_multiplier, 3)
                }
            }
        
        tokenization['category_analysis'] = {
            'content_category': 'digital_art',
            'artistic_skill_score': round(art_factors['artistic_skill'] * 100, 1),
            'concept_originality_score': round(art_factors['concept_originality'] * 100, 1),
            'technical_execution_score': round(art_factors['technical_execution'] * 100, 1),
            'commercial_viability_score': round(art_factors['commercial_viability'] * 100, 1)
        }
        
        return tokenization
    
    def tokenize_generic(self, content_id: str, analysis: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Generic tokenization for other content categories"""
        logger.info(f"Applying generic tokenization for {category} content: {content_id}")
        
        structure = get_category_tokenization_structure(category)
        originality_factor = analysis.get('originality_score', 90) / 100
        
        tokenization = self._create_base_tokenization(content_id, category, analysis)
        
        for category_name, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            token_value = details['base_value'] * originality_factor
            
            tokenization['token_categories'][category_name] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': 1.0
                }
            }
        
        tokenization['category_analysis'] = {
            'content_category': category,
            'tokenization_method': 'generic'
        }
        
        return tokenization
    
    def tokenize_video_games(self, content_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized tokenization for video game content"""
        logger.info(f"Applying video game-specific tokenization for {content_id}")
        
        structure = get_category_tokenization_structure('video_games')
        originality_factor = analysis.get('originality_score', 90) / 100
        
        # Video game-specific analysis factors
        game_factors = {
            'artistic_quality': random.uniform(0.8, 1.0),
            'audio_production': random.uniform(0.7, 0.95),
            'narrative_depth': random.uniform(0.6, 0.9),
            'gameplay_innovation': random.uniform(0.7, 1.0),
            'technical_execution': random.uniform(0.6, 0.95),
            'commercial_potential': random.uniform(0.5, 0.85)
        }
        
        tokenization = self._create_base_tokenization(content_id, 'video_games', analysis)
        
        for category, details in structure.items():
            token_count = int(self.total_tokens * details['percentage'] / 100)
            
            # Apply video game-specific value adjustments
            value_multiplier = 1.0
            if 'visual_art' in category:
                value_multiplier *= game_factors['artistic_quality']
            elif 'audio_music' in category:
                value_multiplier *= game_factors['audio_production']
            elif 'sound_effects' in category:
                value_multiplier *= game_factors['audio_production'] * 0.9  # Slightly lower than music
            elif 'narrative' in category:
                value_multiplier *= game_factors['narrative_depth']
            elif 'gameplay' in category:
                value_multiplier *= game_factors['gameplay_innovation']
            elif 'code_programming' in category:
                value_multiplier *= game_factors['technical_execution']
            elif 'distribution' in category:
                value_multiplier *= game_factors['commercial_potential']
            
            token_value = details['base_value'] * originality_factor * value_multiplier
            
            tokenization['token_categories'][category] = {
                'description': details['description'],
                'token_count': token_count,
                'token_value_usd': round(token_value, 2),
                'total_value_usd': round(token_value * token_count, 2),
                'available_tokens': token_count,
                'sold_tokens': 0,
                'category_factors': {
                    'originality_factor': round(originality_factor, 3),
                    'value_multiplier': round(value_multiplier, 3)
                }
            }
        
        # Add video game-specific metadata
        tokenization['category_analysis'] = {
            'content_category': 'video_games',
            'artistic_quality_score': round(game_factors['artistic_quality'] * 100, 1),
            'audio_production_score': round(game_factors['audio_production'] * 100, 1),
            'narrative_depth_score': round(game_factors['narrative_depth'] * 100, 1),
            'gameplay_innovation_score': round(game_factors['gameplay_innovation'] * 100, 1),
            'technical_execution_score': round(game_factors['technical_execution'] * 100, 1),
            'commercial_potential_score': round(game_factors['commercial_potential'] * 100, 1)
        }
        
        return tokenization
    
    def _create_base_tokenization(self, content_id: str, category: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create base tokenization structure"""
        return {
            'content_id': content_id,
            'content_category': category,
            'total_tokens': self.total_tokens,
            'token_categories': {},
            'created_timestamp': int(time.time()),
            'originality_factor': analysis.get('originality_score', 90) / 100,
            'version': '1.1'
        }
    
    def get_specialized_tokenizer(self, category: str):
        """Get the appropriate tokenization function for a category"""
        tokenizer_map = {
            'film': self.tokenize_film,
            'animation': self.tokenize_animation,
            'screenplay': self.tokenize_screenplay,
            'book_writing': self.tokenize_book_writing,
            'digital_art': self.tokenize_digital_art,
            'video_games': self.tokenize_video_games,
            'photography': lambda cid, analysis: self.tokenize_generic(cid, analysis, 'photography'),
            'music_composition': lambda cid, analysis: self.tokenize_generic(cid, analysis, 'music_composition'),
            'podcast_audio': lambda cid, analysis: self.tokenize_generic(cid, analysis, 'podcast_audio'),
            'software_code': lambda cid, analysis: self.tokenize_generic(cid, analysis, 'software_code')
        }
        
        return tokenizer_map.get(category, lambda cid, analysis: self.tokenize_generic(cid, analysis, category))

def create_specialized_tokenization(content_id: str, analysis: Dict[str, Any], category: str = None, file_extension: str = None) -> Dict[str, Any]:
    """Main function to create specialized tokenization based on content category"""
    
    # Determine category if not provided
    if not category and file_extension:
        category = get_category_by_file_extension(file_extension)
    elif not category:
        category = 'digital_art'  # Default fallback
    
    logger.info(f"Creating specialized tokenization for category: {category}")
    
    tokenizer = SpecializedTokenizer()
    tokenization_func = tokenizer.get_specialized_tokenizer(category)
    
    tokenization = tokenization_func(content_id, analysis)
    
    # Calculate total value
    tokenization['total_value_usd'] = sum(
        cat['total_value_usd'] for cat in tokenization['token_categories'].values()
    )
    
    return tokenization

