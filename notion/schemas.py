import config

DATABASE = {
    "parent": {"page_id": config.NOTION_DATABASE_ID},
    "icon": {"type": "emoji", "emoji": "📝"},
    "is_inline": True,
    "title": [{"type": "text", "text": {"content": "Tittle", "link": None}}],
    "properties": {
        "Name": {"title": {}},
        "Description": {"rich_text": {}},
        "URL": {"url": {}},
        "Seniority": {
            "multi_select": {
                "options": [
                    {"name": "Junior", "color": "green"},
                    {"name": "Mid", "color": "yellow"},
                    {"name": "Senior", "color": "red"},
                ]
            }
        },
        "Tags": {
            "multi_select": {},
        },
    },
}

PAGE = {
    "parent": {"database_id": None},
    "properties": {
        "Name": {
            "title": [
                {"type": "text", "text": {"content": None}},
            ]
        },
        "Description": {"rich_text": [{"type": "text", "text": {"content": None}}]},
        "URL": {"url": None},
        "Seniority": {"multi_select": []},
        "Tags": {"multi_select": []},
    },
}

SEARCH = {"filter": {"value": None, "property": "object"}}

UPDATE = {
    "icon": {"type": "emoji", "emoji": "📙"},
    "properties": {
        "title": {
            "title": [{"type": "text", "text": {"content": "Bookmark-AI-Organizer"}}]
        }
    },
}
