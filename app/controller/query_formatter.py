"""
Provides classes and functions to construct TikTok API query bodies with logical filters (AND, OR, NOT). 
Used by the GUI to build full structured search query body. Also includes default field orders for result formatting

Original Author: Amalie
Refactored, extended & documented by : Elin
Date: 2025-06-28
Version: v2.0.0
"""


class QueryFormatter:
    def query_builder(self, startdate, enddate, args):
        clause_arr = args

        query_structure = {}
        for clause in clause_arr:
            for key, value in clause.items():
                if key in query_structure:
                    query_structure[key].extend(value)
                else:
                    query_structure[key] = value

        query_body = {
            "query": query_structure,
            "start_date": f"{startdate}",
            "end_date": f"{enddate}",
            "cursor": 0,
        }
        return query_body

    def build_clause(self, logic_op, conditions):
        """
        Builds a clause with conditions and the correct boolean operation
        """
        if logic_op not in ["and", "or", "not"]:
            raise ValueError("Needs logic operations: AND/OR/NOT")

        query_clauses = []
        for i in range(len(conditions)):
            if (len(conditions[i])) != 3:
                raise ValueError("Invalid condition format")

            condition = conditions[i]
            field = condition[0]
            value = condition[1]
            operation = condition[2]

            clause = {
                "operation": f"{operation}",
                "field_name": f"{field}",
                "field_values": value if isinstance(value, list) else [value],
            }
            query_clauses.append(clause)
        query = {f"{logic_op}": query_clauses}
        return query

    """
    Takes in list of tuples (field_name, field_value, operation)
    And sends it to build_clause with correct AND/OR/NOT
    """

    def query_AND_clause(self, conditions):
        return self.build_clause("and", conditions)

    # Functions below are the same as above, with respective logical operations
    def query_OR_clause(self, conditions):
        return self.build_clause("or", conditions)

    def query_NOT_clause(self, conditions):
        return self.build_clause("not", conditions)


# Added varibales for Gui ver.2
preferred_order_video = [
    "id",
    "username",
    "region_code",
    "create_time",
    "video_description",
    "video_duration",
    "view_count",
    "like_count",
    "comment_count",
    "share_count",
    "music_id",
    "playlist_id",
    "voice_to_text",
    "hashtag_names",
    "hashtag_info_list",
    "effect_ids",
    "effect_info_list",
    "video_mention_list",
    "video_label",
    "video_tag",
    "is_stem_verified",
    "sticker_info_list",
]

preferred_order_comment = [
    "text",
    "like_count",
    "reply_count",
    "create_time",
    "id",
    "parent_comment_id",
    "video_id",
]

preferred_order_userinfo = [
    "username",
    "display_name",
    "bio_description",
    "avatar_url",
    "is_verified",
    "follower_count",
    "following_count",
    "likes_count",
    "video_count",
]
