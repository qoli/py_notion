
================================================================================
表名: block
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- space_id             TEXT       NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- type                 TEXT       NOT NULL
- properties           TEXT       
- content              TEXT       
- discussions          TEXT       
- view_ids             TEXT       
- collection_id        TEXT       
- permissions          TEXT       
- created_time         REAL       
- last_edited_time     REAL       
- copied_from          TEXT       
- file_ids             TEXT       
- ignore_block_count   INTEGER    
- is_template          INTEGER    
- parent_id            TEXT       
- parent_table         TEXT       
- alive                INTEGER    NOT NULL
- moved                TEXT       
- format               TEXT       
- created_by           TEXT       
- last_edited_by       TEXT       
- created_by_table     TEXT       
- created_by_id        TEXT       
- last_edited_by_table TEXT       
- last_edited_by_id    TEXT       
- content_classification TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_last_access_timestamp REAL       NOT NULL
- meta_role            TEXT       
- moved_to_trash_table TEXT       
- moved_to_trash_id    TEXT       
- moved_to_trash_time  BIGINT     
- deleted_from_trash_time BIGINT     
- deleted_from_trash_table TEXT       
- deleted_from_trash_id TEXT       
- non_content_children TEXT       
- crdt_format_version  INTEGER    
- crdt_data            TEXT       

索引:
----------------------------------------
- lru_deletion_order (0)
- block_parent_id (0)
- sqlite_autoindex_block_1 (1)

示例數據:
----------------------------------------
| c5674aba-fd04-4c2a-9a5a-36e65b825a4b | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 2.0 | None | text | {"title":[["Click here to automatically apply y... | None | None | None | None | None | 1639420719411.0 | 1639420680000.0 | None | None | None | None | beaf3153-b730-4323-b40f-97e43787af6f | block | 1 | None | None | None | None | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | 1686951827764.0 | editor | None | None | None | None | None | None | None | None | None |
| 9be3c877-0fe8-43d5-a274-5d1cc4915b18 | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 2.0 | None | code | {"title":[["License Name: wong qoli\nLicense Ke... | None | None | None | None | None | 1639420719411.0 | 1639420680000.0 | None | None | None | None | beaf3153-b730-4323-b40f-97e43787af6f | block | 1 | None | {"code_wrap":true} | None | None | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | 1686951827764.0 | editor | None | None | None | None | None | None | None | None | None |
| eddb574b-8d0d-419c-9a9d-39bb43b7bc3c | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 4.0 | None | text | {"title":[["qoli wong"]]} | None | None | None | None | None | 1598558064378.0 | 1686951876770.0 | None | None | None | None | beaf3153-b730-4323-b40f-97e43787af6f | block | 0 | None | None | None | None | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | 1686951876771.0 | editor | None | None | None | None | None | None | None | None | None |


================================================================================
表名: collection
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- name                 TEXT       
- description          TEXT       
- icon                 TEXT       
- cover                TEXT       
- schema               TEXT       
- format               TEXT       
- parent_id            TEXT       NOT NULL
- parent_table         TEXT       NOT NULL
- alive                INTEGER    NOT NULL
- file_ids             TEXT       
- template_pages       TEXT       
- copied_from          TEXT       
- migrated             INTEGER    
- space_id             TEXT       NOT NULL
- deleted_schema       TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_collection_1 (1)

示例數據:
----------------------------------------
| 86105f96-12a9-4f4f-8946-338726ba1393 | 3.0 | None | None | None | None | None | {"YWsQ":{"name":"Tags","type":"multi_select"},"... | {"collection_page_properties":[{"visible":true,... | 9dc25c49-4f2a-44e1-b45a-7ed87f42e535 | block | 1 | None | None | None | 1 | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |
| 49994d5c-f375-4839-bfb0-b36b2d976178 | 5.0 | None | None | None | None | None | None | {"uri":"https://github.com/qoli/Syncnext/pulls"... | 12b4a32c-4bd7-44b4-907a-a6bdfea7d2d1 | block | 1 | None | None | None | 1 | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |
| 80a63ff5-5d14-4c0d-8f3c-3756e9d6d1c1 | 27.0 | None | [["Config"]] | None | None | None | {"YpzT":{"name":"Tags","type":"multi_select"},"... | {"collection_page_properties":[{"visible":true,... | 77a72ff3-fe58-499e-82bb-a32d6d255cc4 | block | 1 | None | None | None | 1 | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |


================================================================================
表名: collection_view
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- type                 TEXT       NOT NULL
- name                 TEXT       
- icon                 TEXT       
- page_sort            TEXT       
- parent_id            TEXT       NOT NULL
- parent_table         TEXT       NOT NULL
- alive                INTEGER    NOT NULL
- format               TEXT       
- query2               TEXT       
- space_id             TEXT       NOT NULL
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_collection_view_1 (1)

示例數據:
----------------------------------------
| 5be560ff-c622-417e-adcf-071b9e108dc0 | 3.0 | None | table |  | None | None | da1a91b2-97ea-4e49-9576-43930f27c0b8 | block | 0 | {"table_properties":[{"width":167,"visible":tru... | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |
| 57745c13-5346-408e-8ad2-1b711e8d3f20 | 6.0 | None | table | None | None | ["1e821402-7d0a-4abe-9fc9-66e457a28467","c6c6ca... | 3c4ecfc5-4123-4ee5-88dd-bbd36e0b516d | block | 1 | {"table_wrap":true,"table_properties":[{"width"... | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |
| a757b899-86a9-4141-93f6-57614942fcbe | 2.0 | None | page | Home | None | None | 054f7bfd-6aa4-48fb-b9a6-f8ec310ac32f | block | 0 | {"page_pointer":{"id":"054f7bfd-6aa4-48fb-b9a6-... | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |


================================================================================
表名: comment
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              INTEGER    NOT NULL
- last_version         INTEGER    
- parent_id            TEXT       NOT NULL
- parent_table         TEXT       NOT NULL
- text                 TEXT       
- created_time         REAL       NOT NULL
- last_edited_time     REAL       
- alive                INTEGER    NOT NULL
- created_by_table     TEXT       
- created_by_id        TEXT       
- space_id             TEXT       NOT NULL
- content              TEXT       
- reactions            TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_comment_1 (1)

示例數據:
----------------------------------------
| d0768f88-fba5-45ce-bfb5-ecae705d0623 | 4 | None | 502bb169-ff4e-43b4-88bb-6dfa26f877ee | discussion | [["请问怎么加入测试?"]] | 1686214348756.0 | 1686214320000.0 | 1 | notion_user | 2452f273-bde9-495d-9794-9a1255ab3702 | 1f25848e-bcf9-41ae-b0c9-0afbef0703b2 | None | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |


================================================================================
表名: custom_emoji
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- space_id             TEXT       NOT NULL
- name                 TEXT       NOT NULL
- url                  TEXT       NOT NULL
- file_ids             TEXT       
- created_time         REAL       NOT NULL
- created_by_id        TEXT       NOT NULL
- created_by_table     TEXT       NOT NULL
- alive                INTEGER    NOT NULL
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_custom_emoji_1 (1)


================================================================================
表名: discussion
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              INTEGER    NOT NULL
- last_version         INTEGER    
- parent_id            TEXT       NOT NULL
- parent_table         TEXT       NOT NULL
- context              TEXT       
- resolved             INTEGER    NOT NULL
- comments             TEXT       
- space_id             TEXT       NOT NULL
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL
- type                 TEXT       
- reactions            TEXT       
- property_id          TEXT       

索引:
----------------------------------------
- sqlite_autoindex_discussion_1 (1)

示例數據:
----------------------------------------
| 502bb169-ff4e-43b4-88bb-6dfa26f877ee | 3 | None | 7dcc536d-756a-4a72-84bd-1e6fddc64481 | block | None | 1 | ["d0768f88-fba5-45ce-bfb5-ecae705d0623"] | 1f25848e-bcf9-41ae-b0c9-0afbef0703b2 | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor | default | None | None |


================================================================================
表名: key_value_store
================================================================================

列定義:
----------------------------------------
- id                   INTEGER    PRIMARY KEY
- key                  TEXT       
- value                TEXT       

索引:
----------------------------------------
- sqlite_autoindex_key_value_store_1 (1)


================================================================================
表名: notification
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              INTEGER    NOT NULL
- last_version         INTEGER    
- user_id              TEXT       NOT NULL
- activity_id          TEXT       NOT NULL
- received             INTEGER    NOT NULL
- read                 INTEGER    NOT NULL
- visited              INTEGER    NOT NULL
- emailed              INTEGER    NOT NULL
- invalid              INTEGER    NOT NULL
- space_id             TEXT       NOT NULL
- navigable_block_id   TEXT       
- collection_id        TEXT       
- type                 TEXT       NOT NULL
- end_time             TEXT       NOT NULL
- channel              TEXT       
- archived_at          INTEGER    
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL
- discussion_id        TEXT       

索引:
----------------------------------------
- sqlite_autoindex_notification_1 (1)


================================================================================
表名: notion
================================================================================

列定義:
----------------------------------------
- id                   INTEGER    PRIMARY KEY
- key                             
- value                           

索引:
----------------------------------------
- sqlite_autoindex_notion_1 (1)


================================================================================
表名: notion_user
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- email                TEXT       NOT NULL
- given_name           TEXT       
- family_name          TEXT       
- name                 TEXT       
- profile_photo        TEXT       
- onboarding_completed INTEGER    
- mobile_onboarding_completed INTEGER    
- clipper_onboarding_completed INTEGER    
- reverify             INTEGER    
- is_banned            INTEGER    
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL
- suspended_time       REAL       

索引:
----------------------------------------
- sqlite_autoindex_notion_user_1 (1)

示例數據:
----------------------------------------
| 88f74748-5bb2-4ed6-9b15-f2164687910c | 16.0 | None | fuad@pitch.io | Fuad | Saud | Fuad | https://lh3.googleusercontent.com/a-/AOh14GhZYu... | 1 | 1 | None | 1 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | reader | None |
| 802b62fe-0018-480d-bf85-6e3682c74898 | 12.0 | None | scott@dovetail.com | None | None | Scott Sidwell | https://s3-us-west-2.amazonaws.com/public.notio... | 1 | 1 | None | None | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | reader | None |
| 456c0341-9839-4cae-b24c-ef3e5bab2915 | 15.0 | None | asdf17128@gmail.com | Siyuan | Qin | Siyuan Qin | None | 1 | 1 | 1 | None | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | reader | None |


================================================================================
表名: offline_action
================================================================================

列定義:
----------------------------------------
- id                   INTEGER    PRIMARY KEY
- meta_user_id         TEXT       NOT NULL
- origin_page_id       TEXT       NOT NULL
- impacted_page_id     TEXT       NOT NULL
- autosync_type        TEXT       NOT NULL DEFAULT 'not_autosynced'

索引:
----------------------------------------
- idx_offline_action_impacted_page_id (0)
- idx_offline_action_origin_page_id (0)
- sqlite_autoindex_offline_action_1 (1)

外鍵:
----------------------------------------
- impacted_page_id -> offline_page.id
- meta_user_id -> offline_page.meta_user_id
- origin_page_id -> offline_page.id
- meta_user_id -> offline_page.meta_user_id


================================================================================
表名: offline_page
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- last_downloaded_at   bigint     
- type                 TEXT       
- download_status      TEXT       
- collection_status    TEXT       
- offline_actions      TEXT       
- last_downloaded_version REAL       

索引:
----------------------------------------
- offline_page_download_status_index (0)
- offline_page_type_index (0)
- sqlite_autoindex_offline_page_1 (1)


================================================================================
表名: reaction
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- space_id             TEXT       NOT NULL
- version              INTEGER    NOT NULL
- last_version         INTEGER    
- created_time         REAL       
- parent_table         TEXT       NOT NULL
- parent_id            TEXT       NOT NULL
- icon                 TEXT       NOT NULL
- actors               TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_reaction_1 (1)


================================================================================
表名: records
================================================================================

列定義:
----------------------------------------
- record_table         TEXT       PRIMARY KEY
- record_id            TEXT       PRIMARY KEY
- record_value         TEXT       
- timestamp            NUMERIC    
- parent_table         TEXT       
- parent_id            TEXT       
- importance           NUMERIC    
- user_id              TEXT       PRIMARY KEY
- is_offline                      
- space_id             TEXT       

索引:
----------------------------------------
- record_parent (0)
- record_lru_deletion_order (0)
- sqlite_autoindex_records_1 (1)

示例數據:
----------------------------------------
| page_visit | a8400f0a-b1be-4914-8fd7-b4d5967c126f | {"value":{"id":"a8400f0a-b1be-4914-8fd7-b4d5967... | 1741762892361 | block | efa6a396-e385-4a25-92a8-8f787b9c4a19 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 |
| bot | 59724edc-6fc1-4f92-a769-bcd52a17b97b | {"value":{"id":"59724edc-6fc1-4f92-a769-bcd52a1... | 1741762892465 | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 |
| bot | 0fa650c3-3f0d-47f9-825b-1feff9674750 | {"value":{"id":"0fa650c3-3f0d-47f9-825b-1feff96... | 1741762892465 | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 |


================================================================================
表名: space
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- name                 TEXT       
- permission_groups    TEXT       
- email_domains        TEXT       
- pages                TEXT       
- icon                 TEXT       
- disable_public_access INTEGER    
- disable_public_access_requests INTEGER    
- disable_guests       INTEGER    
- disable_move_to_space INTEGER    
- disable_export       INTEGER    
- disable_space_page_edits INTEGER    
- beta_enabled         INTEGER    
- created_time         REAL       
- last_edited_time     REAL       
- deleted_by           TEXT       
- created_by_table     TEXT       
- created_by_id        TEXT       
- last_edited_by_table TEXT       
- last_edited_by_id    TEXT       
- admin_disable_public_access INTEGER    
- space_pages          TEXT       
- plan_type            TEXT       
- invite_link_enabled  INTEGER    
- initial_use_cases    TEXT       
- public_home_page     TEXT       
- bot_settings         TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       
- settings             TEXT       
- subscription_tier    TEXT       
- disable_team_creation BOOLEAN    
- overdue_subscription TEXT       
- short_id             NUMBER     
- permanently_deleted_time NUMBER     
- short_id_str         TEXT       

索引:
----------------------------------------
- sqlite_autoindex_space_1 (1)

示例數據:
----------------------------------------
| 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | 355.0 | None | 黃佁媛 | None | None | ["8de7a69c-721d-43c9-b135-b1f986a751d3","b77364... | https://s3-us-west-2.amazonaws.com/public.notio... | 0 | None | 0 | 0 | 0 | None | 0 | 1569664920000.0 | 1741687748056.0 | None | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | None | personal | 0 | None | 821b8037-8be2-4114-9fa5-e9a1bbf6cfdc | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor | {"grant_awards":[{"id":"ai.grant032023","featur... | student | None | None | 51996181505 | None | 51996181505 |
| 1f25848e-bcf9-41ae-b0c9-0afbef0703b2 | 70.0 | None | 樣本工作室 | None | None | ["6e520125-6e6c-4be3-93ed-07c7b575eb14"] | None | None | None | None | None | None | None | 0 | 1582440225248.0 | 1582444020000.0 | None | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | notion_user | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | None | None | personal | 0 | None | None | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor | {"in_ai_program":true,"space_survey_data":{"int... | student | None | None | 29654321904 | None | 29654321904 |


================================================================================
表名: space_permission_group
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              INTEGER    NOT NULL
- space_id             TEXT       NOT NULL
- group_id             TEXT       NOT NULL
- name                 TEXT       NOT NULL
- icon                 TEXT       
- created_by_id        TEXT       
- created_by_table     TEXT       
- created_at           REAL       
- last_edited_by_id    TEXT       
- last_edited_by_table TEXT       
- last_edited_at       REAL       
- deleted_at           REAL       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL
- last_version         INTEGER    

索引:
----------------------------------------
- sqlite_autoindex_space_permission_group_1 (1)


================================================================================
表名: space_permission_group_member
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              INTEGER    NOT NULL
- space_id             TEXT       NOT NULL
- space_permission_group_id TEXT       NOT NULL
- user_id              TEXT       NOT NULL
- removed_at           REAL       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL
- last_version         INTEGER    

索引:
----------------------------------------
- sqlite_autoindex_space_permission_group_member_1 (1)


================================================================================
表名: space_user
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- user_id              TEXT       NOT NULL
- space_id             TEXT       NOT NULL
- invite_id            TEXT       
- membership_type      TEXT       NOT NULL
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_space_user_1 (1)


================================================================================
表名: space_view
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- space_id             TEXT       NOT NULL
- bookmarked_pages     TEXT       
- shared_pages         TEXT       
- visited_templates    TEXT       
- sidebar_hidden_templates TEXT       
- notify_mobile        INTEGER    NOT NULL
- notify_desktop       INTEGER    NOT NULL
- notify_email         INTEGER    NOT NULL
- notify_email_always  INTEGER    
- created_getting_started INTEGER    
- parent_id            TEXT       NOT NULL
- parent_table         TEXT       NOT NULL
- alive                INTEGER    NOT NULL
- created_onboarding_templates INTEGER    
- private_pages        TEXT       
- joined               INTEGER    
- joined_teams         TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       
- settings             TEXT       
- ai_suggestions       TEXT       
- sidebar_order        TEXT       
- shared_pages_manual_sort TEXT       
- first_joined_space_time NUMBER     
- assistant_session_starters TEXT       

索引:
----------------------------------------
- sqlite_autoindex_space_view_1 (1)

示例數據:
----------------------------------------
| 0190070c-83fe-4315-ba0f-32d46045f7db | 13.0 | None | 1f25848e-bcf9-41ae-b0c9-0afbef0703b2 | None | None | None | None | 1 | 1 | 1 | None | 1 | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | user_root | 1 | None | None | 1 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor | {"personal_home":{"version":36,"hide_new_badge"... | None | None | None | 0 | None |
| 688842ba-8e47-4abb-a080-08402b82c03a | 112.0 | None | 7cffb4a2-dac8-458f-bc10-c219eb726bb5 | ["1a8c1b36-c401-80f1-bb11-ee6cecbc60ef","19ec1b... | None | ["88c9c2b0-d732-4342-8963-0580a4725571","45d8ee... | ["ba43b46e-4ad3-47f7-95f0-58a3ba01476f"] | 1 | 1 | 0 | None | 1 | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | user_root | 1 | None | ["19ec1b36-c401-80b1-840b-f86f42d690f1","07884d... | 1 | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor | {"personal_home":{"version":36,"hide_new_badge"... | None | None | None | 0 | ["1b3c1b36-c401-804d-9f2d-008634fff9bf","1b1c1b... |


================================================================================
表名: sqlite_sequence
================================================================================

列定義:
----------------------------------------
- name                            
- seq                             

示例數據:
----------------------------------------
| offline_action | 0 |


================================================================================
表名: sqlite_stat1
================================================================================

列定義:
----------------------------------------
- tbl                             
- idx                             
- stat                            

示例數據:
----------------------------------------
| block | lru_deletion_order | 1514 22 |
| block | block_parent_id | 1514 20 20 |
| block | sqlite_autoindex_block_1 | 1514 1 1 |


================================================================================
表名: sqlite_stat4
================================================================================

列定義:
----------------------------------------
- tbl                             
- idx                             
- neq                             
- nlt                             
- ndlt                            
- sample                          


================================================================================
表名: team
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- last_version         REAL       
- space_id             TEXT       NOT NULL
- name                 TEXT       NOT NULL
- description          TEXT       
- icon                 TEXT       
- created_time         REAL       NOT NULL
- created_by_table     TEXT       NOT NULL
- created_by_id        TEXT       NOT NULL
- last_edited_time     REAL       
- last_edited_by_table TEXT       
- last_edited_by_id    TEXT       
- archived_by          TEXT       
- team_pages           TEXT       
- parent_id            TEXT       NOT NULL
- parent_table         TEXT       NOT NULL
- settings             TEXT       
- is_default           INTEGER    
- membership           TEXT       
- permissions          TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       
- pinned_pages         TEXT       
- archived_at          REAL       

索引:
----------------------------------------
- sqlite_autoindex_team_1 (1)


================================================================================
表名: transactions
================================================================================

列定義:
----------------------------------------
- id                   TEXT       NOT NULL
- user_id              TEXT       
- space_id             TEXT       
- operations           TEXT       NOT NULL
- timestamp            REAL       NOT NULL
- debug                TEXT       

索引:
----------------------------------------
- transactions_user_id (0)


================================================================================
表名: user_root
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              REAL       NOT NULL
- space_views          TEXT       
- left_spaces          TEXT       
- space_view_pointers  TEXT       
- deleted_email        TEXT       
- last_version         REAL       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_user_root_1 (1)

示例數據:
----------------------------------------
| 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | 39.0 | ["688842ba-8e47-4abb-a080-08402b82c03a","019007... | ["f4b0cbc5-e101-4bb2-b71c-a35abb97f3ce","770eea... | [{"id":"688842ba-8e47-4abb-a080-08402b82c03a","... | None | None | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |


================================================================================
表名: user_settings
================================================================================

列定義:
----------------------------------------
- id                   TEXT       PRIMARY KEY NOT NULL
- version              INTEGER    NOT NULL
- last_version         INTEGER    
- settings             TEXT       
- meta_user_id         TEXT       PRIMARY KEY NOT NULL
- meta_role            TEXT       NOT NULL

索引:
----------------------------------------
- sqlite_autoindex_user_settings_1 (1)

示例數據:
----------------------------------------
| 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | 1269 | None | {"type":"personal","locale":"en-US","persona":"... | 7746ede7-d72f-4941-9c2a-d8da0ee5bbff | editor |

