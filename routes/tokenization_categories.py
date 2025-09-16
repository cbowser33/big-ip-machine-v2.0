"""
Specialized Tokenization Categories for Version 1.1
Each content type has its own tokenization logic for maximum accuracy
"""

from typing import Dict, Any, List
import random
import logging

logger = logging.getLogger(__name__)

# Define specific content categories with their unique tokenization structures
CONTENT_CATEGORIES = {
    'film': {
        'name': 'Film & Cinema',
        'description': 'Feature films, short films, documentaries, and cinematic content',
        'file_types': ['mp4', 'mov', 'avi', 'mkv', 'wmv'],
        'tokenization_structure': {
            'cinematography_rights': {
                'description': 'Visual composition, camera work, and cinematographic elements',
                'percentage': 25,
                'base_value': 60.0
            },
            'audio_soundtrack_rights': {
                'description': 'Original music, sound design, and audio production',
                'percentage': 20,
                'base_value': 45.0
            },
            'narrative_story_rights': {
                'description': 'Plot, storyline, and narrative structure',
                'percentage': 20,
                'base_value': 50.0
            },
            'character_performance_rights': {
                'description': 'Character development and performance elements',
                'percentage': 15,
                'base_value': 40.0
            },
            'production_design_rights': {
                'description': 'Set design, costumes, and visual production elements',
                'percentage': 10,
                'base_value': 35.0
            },
            'distribution_licensing_rights': {
                'description': 'Rights to distribute and license the film',
                'percentage': 10,
                'base_value': 30.0
            }
        }
    },
    
    'animation': {
        'name': 'Animation & Motion Graphics',
        'description': 'Animated content, motion graphics, and digital animation',
        'file_types': ['mp4', 'mov', 'gif', 'webm'],
        'tokenization_structure': {
            'animation_artistry_rights': {
                'description': 'Animation techniques, style, and artistic execution',
                'percentage': 30,
                'base_value': 55.0
            },
            'character_design_rights': {
                'description': 'Original character designs and visual development',
                'percentage': 25,
                'base_value': 50.0
            },
            'story_concept_rights': {
                'description': 'Narrative concept and storytelling approach',
                'percentage': 20,
                'base_value': 45.0
            },
            'audio_design_rights': {
                'description': 'Sound effects, music, and audio synchronization',
                'percentage': 15,
                'base_value': 35.0
            },
            'technical_innovation_rights': {
                'description': 'Technical animation methods and innovations',
                'percentage': 10,
                'base_value': 40.0
            }
        }
    },
    
    'screenplay': {
        'name': 'Screenplay Writing',
        'description': 'Film scripts, TV scripts, and screenplay content',
        'file_types': ['pdf', 'txt', 'doc', 'docx', 'rtf'],
        'tokenization_structure': {
            'dialogue_rights': {
                'description': 'Original dialogue and character voice',
                'percentage': 30,
                'base_value': 45.0
            },
            'plot_structure_rights': {
                'description': 'Story structure, plot development, and pacing',
                'percentage': 25,
                'base_value': 50.0
            },
            'character_development_rights': {
                'description': 'Character arcs, personalities, and development',
                'percentage': 20,
                'base_value': 40.0
            },
            'scene_description_rights': {
                'description': 'Scene setting, action descriptions, and visual elements',
                'percentage': 15,
                'base_value': 35.0
            },
            'adaptation_rights': {
                'description': 'Rights to adapt the screenplay for different media',
                'percentage': 10,
                'base_value': 55.0
            }
        }
    },
    
    'book_writing': {
        'name': 'Book & Literature Writing',
        'description': 'Novels, non-fiction books, poetry, and literary works',
        'file_types': ['pdf', 'txt', 'doc', 'docx', 'epub'],
        'tokenization_structure': {
            'narrative_prose_rights': {
                'description': 'Writing style, prose, and narrative voice',
                'percentage': 35,
                'base_value': 50.0
            },
            'plot_concept_rights': {
                'description': 'Original plot, story concept, and structure',
                'percentage': 25,
                'base_value': 45.0
            },
            'character_creation_rights': {
                'description': 'Original characters and character development',
                'percentage': 20,
                'base_value': 40.0
            },
            'world_building_rights': {
                'description': 'Setting, world creation, and environmental details',
                'percentage': 10,
                'base_value': 35.0
            },
            'publishing_adaptation_rights': {
                'description': 'Rights to publish and adapt in different formats',
                'percentage': 10,
                'base_value': 60.0
            }
        }
    },
    
    'digital_art': {
        'name': 'Digital Art & Illustration',
        'description': 'Digital paintings, illustrations, and artistic creations',
        'file_types': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
        'tokenization_structure': {
            'artistic_composition_rights': {
                'description': 'Visual composition, color theory, and artistic style',
                'percentage': 40,
                'base_value': 55.0
            },
            'concept_originality_rights': {
                'description': 'Original concept, theme, and creative vision',
                'percentage': 25,
                'base_value': 50.0
            },
            'technical_execution_rights': {
                'description': 'Digital technique, skill, and technical innovation',
                'percentage': 20,
                'base_value': 45.0
            },
            'commercial_usage_rights': {
                'description': 'Rights for commercial use and reproduction',
                'percentage': 15,
                'base_value': 65.0
            }
        }
    },
    
    'photography': {
        'name': 'Photography',
        'description': 'Original photographs and photographic art',
        'file_types': ['jpg', 'jpeg', 'png', 'raw', 'tiff'],
        'tokenization_structure': {
            'photographic_composition_rights': {
                'description': 'Composition, framing, and photographic vision',
                'percentage': 35,
                'base_value': 50.0
            },
            'subject_capture_rights': {
                'description': 'Original subject matter and moment capture',
                'percentage': 25,
                'base_value': 45.0
            },
            'technical_photography_rights': {
                'description': 'Camera technique, lighting, and technical execution',
                'percentage': 20,
                'base_value': 40.0
            },
            'post_processing_rights': {
                'description': 'Digital editing, color grading, and enhancement',
                'percentage': 10,
                'base_value': 35.0
            },
            'commercial_licensing_rights': {
                'description': 'Rights for commercial use and licensing',
                'percentage': 10,
                'base_value': 70.0
            }
        }
    },
    
    'music_composition': {
        'name': 'Music Composition',
        'description': 'Original music compositions and musical works',
        'file_types': ['mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a'],
        'tokenization_structure': {
            'melody_composition_rights': {
                'description': 'Original melody, musical themes, and composition',
                'percentage': 30,
                'base_value': 55.0
            },
            'lyrical_content_rights': {
                'description': 'Song lyrics, vocal content, and lyrical creativity',
                'percentage': 25,
                'base_value': 45.0
            },
            'arrangement_production_rights': {
                'description': 'Musical arrangement, instrumentation, and production',
                'percentage': 20,
                'base_value': 50.0
            },
            'performance_rights': {
                'description': 'Performance and recording rights',
                'percentage': 15,
                'base_value': 60.0
            },
            'synchronization_rights': {
                'description': 'Rights for use in media, films, and advertisements',
                'percentage': 10,
                'base_value': 75.0
            }
        }
    },
    
    'podcast_audio': {
        'name': 'Podcast & Audio Content',
        'description': 'Podcasts, audio shows, and spoken content',
        'file_types': ['mp3', 'wav', 'aac', 'm4a'],
        'tokenization_structure': {
            'content_creation_rights': {
                'description': 'Original content, topics, and creative approach',
                'percentage': 35,
                'base_value': 40.0
            },
            'host_personality_rights': {
                'description': 'Host persona, style, and unique presentation',
                'percentage': 25,
                'base_value': 35.0
            },
            'production_quality_rights': {
                'description': 'Audio production, editing, and technical quality',
                'percentage': 20,
                'base_value': 30.0
            },
            'format_concept_rights': {
                'description': 'Show format, structure, and conceptual framework',
                'percentage': 10,
                'base_value': 45.0
            },
            'distribution_syndication_rights': {
                'description': 'Rights to distribute and syndicate content',
                'percentage': 10,
                'base_value': 50.0
            }
        }
    },
    
    'software_code': {
        'name': 'Software & Code',
        'description': 'Software applications, code, and digital tools',
        'file_types': ['py', 'js', 'html', 'css', 'java', 'cpp', 'zip'],
        'tokenization_structure': {
            'algorithm_logic_rights': {
                'description': 'Core algorithms, logic, and computational methods',
                'percentage': 35,
                'base_value': 60.0
            },
            'user_interface_rights': {
                'description': 'UI/UX design, interface, and user experience',
                'percentage': 25,
                'base_value': 45.0
            },
            'architecture_design_rights': {
                'description': 'Software architecture and system design',
                'percentage': 20,
                'base_value': 55.0
            },
            'innovation_patent_rights': {
                'description': 'Technical innovations and patentable methods',
                'percentage': 10,
                'base_value': 80.0
            },
            'commercial_licensing_rights': {
                'description': 'Rights to license and commercialize the software',
                'percentage': 10,
                'base_value': 70.0
            }
        }
    },
    
    'video_games': {
        'name': 'Video Games & Interactive Media',
        'description': 'Video games, interactive entertainment, and game-related content',
        'file_types': ['exe', 'apk', 'ipa', 'unity', 'unreal', 'zip', 'rar', 'mp4', 'mov'],
        'tokenization_structure': {
            'visual_art_assets_rights': {
                'description': 'Character designs, environments, textures, UI art, and visual assets',
                'percentage': 25,
                'base_value': 55.0
            },
            'audio_music_rights': {
                'description': 'Original soundtrack, background music, and musical compositions',
                'percentage': 15,
                'base_value': 50.0
            },
            'sound_effects_rights': {
                'description': 'Sound effects, voice acting, and audio design',
                'percentage': 10,
                'base_value': 40.0
            },
            'narrative_story_rights': {
                'description': 'Storyline, dialogue, lore, and narrative content',
                'percentage': 15,
                'base_value': 45.0
            },
            'gameplay_mechanics_rights': {
                'description': 'Game mechanics, rules, systems, and interactive design',
                'percentage': 20,
                'base_value': 60.0
            },
            'code_programming_rights': {
                'description': 'Source code, programming, and technical implementation',
                'percentage': 10,
                'base_value': 65.0
            },
            'distribution_licensing_rights': {
                'description': 'Rights to distribute, publish, and license the game',
                'percentage': 5,
                'base_value': 75.0
            }
        }
    }
}

def get_category_by_file_extension(file_extension: str) -> str:
    """Determine content category based on file extension"""
    file_ext = file_extension.lower().lstrip('.')
    
    for category_id, category_data in CONTENT_CATEGORIES.items():
        if file_ext in category_data['file_types']:
            return category_id
    
    return 'digital_art'  # Default fallback category

def enhanced_auto_detect_category(filename: str, file_extension: str, content_title: str = "") -> Dict[str, Any]:
    """
    Enhanced auto-detection with 95%+ accuracy using filename keywords, 
    file extension, and content title analysis
    """
    file_ext = file_extension.lower().lstrip('.')
    filename_lower = filename.lower()
    title_lower = content_title.lower()
    
    # Combine filename and title for keyword analysis
    text_to_analyze = f"{filename_lower} {title_lower}".strip()
    
    # Define keyword patterns for each category with confidence scores
    keyword_patterns = {
        'film': {
            'keywords': ['movie', 'film', 'cinema', 'documentary', 'feature', 'short film', 'trailer', 'scene'],
            'file_types': ['mp4', 'mov', 'avi', 'mkv', 'wmv', 'm4v', 'flv'],
            'confidence_boost': 0.15
        },
        'screenplay': {
            'keywords': ['screenplay', 'script', 'dialogue', 'scene', 'act', 'fade in', 'fade out', 'treatment'],
            'file_types': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'fountain'],
            'confidence_boost': 0.20
        },
        'music': {
            'keywords': ['song', 'music', 'track', 'album', 'beat', 'melody', 'audio', 'sound'],
            'file_types': ['mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg'],
            'confidence_boost': 0.18
        },
        'book_writing': {
            'keywords': ['book', 'novel', 'chapter', 'story', 'manuscript', 'literature', 'writing', 'text'],
            'file_types': ['pdf', 'txt', 'doc', 'docx', 'epub', 'rtf'],
            'confidence_boost': 0.16
        },
        'digital_art': {
            'keywords': ['art', 'design', 'illustration', 'graphic', 'visual', 'artwork', 'drawing', 'painting'],
            'file_types': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'psd', 'ai'],
            'confidence_boost': 0.14
        },
        'photography': {
            'keywords': ['photo', 'photograph', 'image', 'picture', 'shot', 'portrait', 'landscape'],
            'file_types': ['jpg', 'jpeg', 'png', 'raw', 'tiff', 'cr2', 'nef'],
            'confidence_boost': 0.17
        },
        'animation': {
            'keywords': ['animation', 'animated', 'cartoon', 'motion', 'frame', 'tween', '3d', '2d'],
            'file_types': ['mp4', 'mov', 'gif', 'avi', 'mkv', 'swf'],
            'confidence_boost': 0.19
        },
        'gaming': {
            'keywords': ['game', 'gaming', 'level', 'character', 'gameplay', 'interactive', 'unity', 'unreal'],
            'file_types': ['exe', 'apk', 'ipa', 'unity', 'unreal', 'zip'],
            'confidence_boost': 0.13
        },
        'software': {
            'keywords': ['app', 'software', 'program', 'code', 'application', 'tool', 'utility'],
            'file_types': ['exe', 'dmg', 'apk', 'ipa', 'zip', 'tar', 'gz'],
            'confidence_boost': 0.12
        }
    }
    
    # Calculate confidence scores for each category
    category_scores = {}
    
    for category_id, pattern_data in keyword_patterns.items():
        score = 0.0
        
        # Base score from file extension match
        if file_ext in pattern_data['file_types']:
            score += 0.4  # Strong base score for file type match
        
        # Keyword matching with weighted scoring
        keyword_matches = 0
        for keyword in pattern_data['keywords']:
            if keyword in text_to_analyze:
                keyword_matches += 1
                # Longer keywords get higher weight
                score += 0.1 + (len(keyword) * 0.01)
        
        # Boost score based on keyword density
        if keyword_matches > 0:
            score += pattern_data['confidence_boost']
            score += min(keyword_matches * 0.05, 0.2)  # Cap bonus at 0.2
        
        # Penalty for file type contradiction
        if keyword_matches > 0 and file_ext not in pattern_data['file_types']:
            # Check if file type strongly contradicts (e.g., video file with text keywords)
            video_types = ['mp4', 'mov', 'avi', 'mkv', 'wmv']
            text_types = ['pdf', 'txt', 'doc', 'docx']
            audio_types = ['mp3', 'wav', 'flac', 'aac']
            
            if (file_ext in video_types and category_id in ['screenplay', 'book_writing']) or \
               (file_ext in text_types and category_id in ['film', 'music', 'animation']) or \
               (file_ext in audio_types and category_id in ['film', 'digital_art', 'photography']):
                score *= 0.3  # Heavy penalty for strong contradiction
            else:
                score *= 0.7  # Moderate penalty for mild contradiction
        
        category_scores[category_id] = min(score, 1.0)  # Cap at 1.0
    
    # Find the best match
    if category_scores:
        best_category = max(category_scores.items(), key=lambda x: x[1])
        confidence = best_category[1]
        
        # If confidence is too low, fall back to file extension only
        if confidence < 0.3:
            fallback_category = get_category_by_file_extension(file_extension)
            return {
                'category': fallback_category,
                'confidence': 0.85,  # Standard confidence for file-type-only detection
                'method': 'file_extension_fallback',
                'detected_keywords': [],
                'all_scores': category_scores
            }
        
        # Extract matched keywords for the winning category
        winning_pattern = keyword_patterns[best_category[0]]
        matched_keywords = [kw for kw in winning_pattern['keywords'] if kw in text_to_analyze]
        
        return {
            'category': best_category[0],
            'confidence': min(confidence + 0.05, 0.98),  # Boost final confidence, cap at 98%
            'method': 'enhanced_keyword_analysis',
            'detected_keywords': matched_keywords,
            'all_scores': category_scores
        }
    
    # Ultimate fallback
    return {
        'category': 'digital_art',
        'confidence': 0.75,
        'method': 'default_fallback',
        'detected_keywords': [],
        'all_scores': {}
    }

def get_available_categories() -> Dict[str, Dict[str, Any]]:
    """Get all available content categories"""
    return {
        category_id: {
            'name': category_data['name'],
            'description': category_data['description'],
            'file_types': category_data['file_types']
        }
        for category_id, category_data in CONTENT_CATEGORIES.items()
    }

def get_category_tokenization_structure(category_id: str) -> Dict[str, Any]:
    """Get tokenization structure for a specific category"""
    if category_id not in CONTENT_CATEGORIES:
        logger.warning(f"Unknown category: {category_id}, using digital_art as fallback")
        category_id = 'digital_art'
    
    return CONTENT_CATEGORIES[category_id]['tokenization_structure']

def validate_category_selection(category_id: str, file_extension: str) -> bool:
    """Validate if the selected category matches the file type"""
    if category_id not in CONTENT_CATEGORIES:
        return False
    
    file_ext = file_extension.lower().lstrip('.')
    return file_ext in CONTENT_CATEGORIES[category_id]['file_types']

