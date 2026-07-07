from .schemas import MaterialCreate, MaterialUpdate, MaterialResponse, MaterialListResponse, MaterialAddTags
from .models import Material, Tag
from .repositories import MaterialRepository
from .services import (
    list_materials, get_material, create_material, update_material, delete_material,
    add_tags_to_material, remove_tag_from_material, extract_tags_from_content,
    suggest_tags_for_content, get_tagger_info, get_organizer_info,
)
from .taggers import (
    MaterialTagger, TaggerManager, get_tagger_manager, AIMaterialTagger,
    setup_default_taggers,
)
from .organizers import (
    MaterialOrganizer, OrganizerManager, get_organizer_manager,
)

__all__ = [
    "MaterialCreate",
    "MaterialUpdate",
    "MaterialResponse",
    "MaterialListResponse",
    "MaterialAddTags",
    "Material",
    "Tag",
    "MaterialRepository",
    "list_materials",
    "get_material",
    "create_material",
    "update_material",
    "delete_material",
    "add_tags_to_material",
    "remove_tag_from_material",
    "extract_tags_from_content",
    "suggest_tags_for_content",
    "get_tagger_info",
    "get_organizer_info",
    "MaterialTagger",
    "TaggerManager",
    "get_tagger_manager",
    "AIMaterialTagger",
    "setup_default_taggers",
    "MaterialOrganizer",
    "OrganizerManager",
    "get_organizer_manager",
]
