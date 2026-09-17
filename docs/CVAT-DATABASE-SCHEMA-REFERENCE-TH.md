# CVAT PostgreSQL Schema Reference

เอกสารนี้สร้างจากฐานข้อมูล CVAT ที่กำลังรันอยู่ใน Docker container `cvat_db` เมื่อ 17 กันยายน 2026 เพื่อใช้เป็น reference สำหรับ developer โดยมี 71 ตารางใน schema `public`.

> ใช้อ่านและ monitor เท่านั้น ควรแก้ไขข้อมูลผ่าน CVAT REST API ไม่ควรแก้ตารางโดยตรง เพราะอาจทำให้ cache, storage และข้อมูล annotation ไม่สอดคล้องกัน

## คำสั่งสร้างเอกสารใหม่

```bash
docker compose exec -T cvat_db pg_dump -U root -d cvat --schema-only --no-owner > cvat-schema.sql
```

## ตารางและคอลัมน์ทั้งหมด

### `access_tokens_accesstoken`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `prefix` | `character varying` | NO |  |
| 2 | `hashed_key` | `character varying` | NO |  |
| 3 | `created` | `timestamp with time zone` | NO |  |
| 4 | `name` | `character varying` | NO |  |
| 5 | `revoked` | `boolean` | NO |  |
| 6 | `expiry_date` | `timestamp with time zone` | YES |  |
| 7 | `id` | `integer` | NO |  |
| 8 | `updated_date` | `timestamp with time zone` | NO |  |
| 9 | `last_used_date` | `timestamp with time zone` | YES |  |
| 10 | `read_only` | `boolean` | NO |  |
| 11 | `owner_id` | `integer` | NO |  |

### `account_emailaddress`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `email` | `character varying` | NO |  |
| 3 | `verified` | `boolean` | NO |  |
| 4 | `primary` | `boolean` | NO |  |
| 5 | `user_id` | `integer` | NO |  |

### `account_emailconfirmation`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `created` | `timestamp with time zone` | NO |  |
| 3 | `sent` | `timestamp with time zone` | YES |  |
| 4 | `key` | `character varying` | NO |  |
| 5 | `email_address_id` | `integer` | NO |  |

### `auth_group`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `name` | `character varying` | NO |  |

### `auth_group_permissions`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `group_id` | `integer` | NO |  |
| 3 | `permission_id` | `integer` | NO |  |

### `auth_permission`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `name` | `character varying` | NO |  |
| 3 | `content_type_id` | `integer` | NO |  |
| 4 | `codename` | `character varying` | NO |  |

### `auth_user`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `password` | `character varying` | NO |  |
| 3 | `last_login` | `timestamp with time zone` | YES |  |
| 4 | `is_superuser` | `boolean` | NO |  |
| 5 | `username` | `character varying` | NO |  |
| 6 | `first_name` | `character varying` | NO |  |
| 7 | `last_name` | `character varying` | NO |  |
| 8 | `email` | `character varying` | NO |  |
| 9 | `is_staff` | `boolean` | NO |  |
| 10 | `is_active` | `boolean` | NO |  |
| 11 | `date_joined` | `timestamp with time zone` | NO |  |
| 12 | `created_via` | `character varying` | YES |  |

### `auth_user_groups`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `user_id` | `integer` | NO |  |
| 3 | `group_id` | `integer` | NO |  |

### `auth_user_user_permissions`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `user_id` | `integer` | NO |  |
| 3 | `permission_id` | `integer` | NO |  |

### `authtoken_token`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `key` | `character varying` | NO |  |
| 2 | `created` | `timestamp with time zone` | NO |  |
| 3 | `user_id` | `integer` | NO |  |

### `consensus_consensussettings`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 3 | `iou_threshold` | `double precision` | NO |  |
| 4 | `task_id` | `integer` | NO |  |

### `django_admin_log`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `action_time` | `timestamp with time zone` | NO |  |
| 3 | `object_id` | `text` | YES |  |
| 4 | `object_repr` | `character varying` | NO |  |
| 5 | `action_flag` | `smallint` | NO |  |
| 6 | `change_message` | `text` | NO |  |
| 7 | `content_type_id` | `integer` | YES |  |
| 8 | `user_id` | `integer` | NO |  |

### `django_content_type`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 3 | `app_label` | `character varying` | NO |  |
| 4 | `model` | `character varying` | NO |  |

### `django_migrations`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `app` | `character varying` | NO |  |
| 3 | `name` | `character varying` | NO |  |
| 4 | `applied` | `timestamp with time zone` | NO |  |

### `django_session`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `session_key` | `character varying` | NO |  |
| 2 | `session_data` | `text` | NO |  |
| 3 | `expire_date` | `timestamp with time zone` | NO |  |

### `django_site`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `domain` | `character varying` | NO |  |
| 3 | `name` | `character varying` | NO |  |

### `engine_annotationguide`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `markdown` | `text` | NO |  |
| 3 | `created_date` | `timestamp with time zone` | NO |  |
| 4 | `updated_date` | `timestamp with time zone` | NO |  |
| 5 | `project_id` | `integer` | YES |  |
| 6 | `task_id` | `integer` | YES |  |

### `engine_asset`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `uuid` | `uuid` | NO |  |
| 2 | `filename` | `character varying` | NO |  |
| 3 | `created_date` | `timestamp with time zone` | NO |  |
| 4 | `guide_id` | `integer` | NO |  |
| 5 | `owner_id` | `integer` | YES |  |
| 6 | `content_size` | `bigint` | YES |  |

### `engine_attributespec`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `label_id` | `integer` | NO |  |
| 3 | `default_value` | `character varying` | NO |  |
| 4 | `input_type` | `character varying` | NO |  |
| 5 | `mutable` | `boolean` | NO |  |
| 6 | `name` | `character varying` | NO |  |
| 7 | `values` | `character varying` | NO |  |

### `engine_audio`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `path` | `character varying` | NO |  |
| 3 | `sampling_rate` | `integer` | NO |  |
| 4 | `has_cover_image` | `boolean` | NO |  |
| 5 | `data_id` | `integer` | YES |  |

### `engine_clientfile`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `file` | `character varying` | NO |  |
| 3 | `data_id` | `integer` | YES |  |

### `engine_cloudstorage`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `provider_type` | `character varying` | NO |  |
| 3 | `resource` | `character varying` | NO |  |
| 4 | `display_name` | `character varying` | NO |  |
| 5 | `created_date` | `timestamp with time zone` | NO |  |
| 6 | `updated_date` | `timestamp with time zone` | NO |  |
| 7 | `credentials` | `character varying` | YES |  |
| 8 | `credentials_type` | `character varying` | NO |  |
| 9 | `specific_attributes` | `character varying` | NO |  |
| 10 | `description` | `text` | NO |  |
| 11 | `owner_id` | `integer` | YES |  |
| 12 | `organization_id` | `integer` | YES |  |

### `engine_comment`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `message` | `text` | NO |  |
| 3 | `created_date` | `timestamp with time zone` | NO |  |
| 4 | `updated_date` | `timestamp with time zone` | NO |  |
| 5 | `owner_id` | `integer` | YES |  |
| 6 | `issue_id` | `integer` | NO |  |

### `engine_data`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `chunk_size` | `integer` | YES |  |
| 3 | `size` | `integer` | NO |  |
| 4 | `image_quality` | `smallint` | NO |  |
| 5 | `start_frame` | `integer` | NO |  |
| 6 | `stop_frame` | `integer` | NO |  |
| 7 | `frame_filter` | `character varying` | NO |  |
| 8 | `compressed_chunk_type` | `character varying` | NO |  |
| 9 | `original_chunk_type` | `character varying` | NO |  |
| 10 | `storage_method` | `character varying` | NO |  |
| 11 | `storage` | `character varying` | NO |  |
| 12 | `cloud_storage_id` | `integer` | YES |  |
| 13 | `sorting_method` | `character varying` | NO |  |
| 14 | `deleted_frames` | `text` | NO |  |
| 15 | `content_size` | `bigint` | YES |  |
| 16 | `local_storage_backing_cs_id` | `integer` | YES |  |

### `engine_image`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `path` | `character varying` | NO |  |
| 3 | `frame` | `integer` | NO |  |
| 4 | `height` | `integer` | NO |  |
| 5 | `width` | `integer` | NO |  |
| 6 | `data_id` | `integer` | YES |  |
| 7 | `is_placeholder` | `boolean` | NO |  |
| 8 | `real_frame` | `integer` | NO |  |

### `engine_issue`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `frame` | `integer` | NO |  |
| 3 | `position` | `text` | NO |  |
| 4 | `created_date` | `timestamp with time zone` | NO |  |
| 5 | `updated_date` | `timestamp with time zone` | NO |  |
| 6 | `job_id` | `integer` | NO |  |
| 7 | `owner_id` | `integer` | YES |  |
| 8 | `assignee_id` | `integer` | YES |  |
| 9 | `resolved` | `boolean` | NO |  |
| 10 | `assignee_updated_date` | `timestamp with time zone` | YES |  |

### `engine_job`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `segment_id` | `integer` | NO |  |
| 3 | `assignee_id` | `integer` | YES |  |
| 4 | `status` | `character varying` | NO |  |
| 5 | `stage` | `character varying` | NO |  |
| 6 | `state` | `character varying` | NO |  |
| 7 | `updated_date` | `timestamp with time zone` | NO |  |
| 8 | `type` | `character varying` | NO |  |
| 9 | `created_date` | `timestamp with time zone` | NO |  |
| 10 | `assignee_updated_date` | `timestamp with time zone` | YES |  |
| 11 | `parent_job_id` | `integer` | YES |  |

### `engine_label`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `name` | `character varying` | NO |  |
| 3 | `task_id` | `integer` | YES |  |
| 4 | `color` | `character varying` | NO |  |
| 5 | `project_id` | `integer` | YES |  |
| 6 | `parent_id` | `integer` | YES |  |
| 7 | `type` | `character varying` | NO |  |

### `engine_labeledimage`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `frame` | `integer` | NO |  |
| 3 | `group` | `integer` | YES |  |
| 4 | `job_id` | `integer` | NO |  |
| 5 | `label_id` | `integer` | NO |  |
| 6 | `source` | `character varying` | YES |  |

### `engine_labeledimageattributeval`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `value` | `character varying` | NO |  |
| 3 | `spec_id` | `integer` | NO |  |
| 4 | `image_id` | `bigint` | NO |  |
| 5 | `job_id` | `integer` | NO |  |

### `engine_labeledinterval`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `group` | `integer` | YES |  |
| 3 | `source` | `character varying` | YES |  |
| 4 | `score` | `double precision` | NO |  |
| 5 | `start` | `integer` | NO |  |
| 6 | `stop` | `integer` | YES |  |
| 7 | `job_id` | `integer` | NO |  |
| 8 | `label_id` | `integer` | NO |  |

### `engine_labeledintervalattributeval`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `value` | `character varying` | NO |  |
| 3 | `interval_id` | `bigint` | NO |  |
| 4 | `job_id` | `integer` | NO |  |
| 5 | `spec_id` | `integer` | NO |  |

### `engine_labeledshape`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `frame` | `integer` | NO |  |
| 3 | `group` | `integer` | YES |  |
| 4 | `type` | `character varying` | NO |  |
| 5 | `occluded` | `boolean` | NO |  |
| 6 | `z_order` | `integer` | NO |  |
| 7 | `points` | `text` | NO |  |
| 8 | `job_id` | `integer` | NO |  |
| 9 | `label_id` | `integer` | NO |  |
| 10 | `source` | `character varying` | YES |  |
| 11 | `rotation` | `double precision` | NO |  |
| 12 | `parent_id` | `bigint` | YES |  |
| 13 | `outside` | `boolean` | NO |  |
| 14 | `score` | `double precision` | NO |  |

### `engine_labeledshapeattributeval`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `value` | `character varying` | NO |  |
| 3 | `spec_id` | `integer` | NO |  |
| 4 | `shape_id` | `bigint` | NO |  |
| 5 | `job_id` | `integer` | NO |  |

### `engine_labeledtrack`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `frame` | `integer` | NO |  |
| 3 | `group` | `integer` | YES |  |
| 4 | `job_id` | `integer` | NO |  |
| 5 | `label_id` | `integer` | NO |  |
| 6 | `source` | `character varying` | YES |  |
| 7 | `parent_id` | `bigint` | YES |  |

### `engine_labeledtrackattributeval`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `value` | `character varying` | NO |  |
| 3 | `spec_id` | `integer` | NO |  |
| 4 | `track_id` | `bigint` | NO |  |
| 5 | `job_id` | `integer` | NO |  |

### `engine_manifest`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `filename` | `character varying` | NO |  |
| 3 | `cloud_storage_id` | `integer` | YES |  |

### `engine_profile`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `rating` | `double precision` | NO |  |
| 3 | `user_id` | `integer` | NO |  |
| 4 | `has_analytics_access` | `boolean` | NO |  |
| 5 | `last_activity_date` | `timestamp with time zone` | YES |  |

### `engine_project`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `name` | `character varying` | NO |  |
| 3 | `bug_tracker` | `character varying` | NO |  |
| 4 | `created_date` | `timestamp with time zone` | NO |  |
| 5 | `updated_date` | `timestamp with time zone` | NO |  |
| 6 | `status` | `character varying` | NO |  |
| 7 | `assignee_id` | `integer` | YES |  |
| 8 | `owner_id` | `integer` | YES |  |
| 9 | `organization_id` | `integer` | YES |  |
| 10 | `source_storage_id` | `integer` | YES |  |
| 11 | `target_storage_id` | `integer` | YES |  |
| 12 | `assignee_updated_date` | `timestamp with time zone` | YES |  |

### `engine_relatedfile`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `path` | `character varying` | NO |  |
| 3 | `data_id` | `integer` | YES |  |

### `engine_relatedfile_images`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `relatedfile_id` | `integer` | NO |  |
| 3 | `image_id` | `integer` | NO |  |

### `engine_remotefile`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `file` | `character varying` | NO |  |
| 3 | `data_id` | `integer` | YES |  |

### `engine_segment`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `start_frame` | `integer` | NO |  |
| 3 | `stop_frame` | `integer` | NO |  |
| 4 | `task_id` | `integer` | NO |  |
| 5 | `frames` | `text` | NO |  |
| 6 | `type` | `character varying` | NO |  |
| 7 | `chunks_updated_date` | `timestamp with time zone` | NO |  |

### `engine_serverfile`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `file` | `character varying` | NO |  |
| 3 | `data_id` | `integer` | YES |  |

### `engine_skeleton`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `svg` | `text` | YES |  |
| 3 | `root_id` | `integer` | NO |  |

### `engine_storage`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `location` | `character varying` | NO |  |
| 3 | `cloud_storage_id` | `integer` | YES |  |

### `engine_task`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `name` | `character varying` | NO |  |
| 4 | `mode` | `character varying` | NO |  |
| 5 | `created_date` | `timestamp with time zone` | NO |  |
| 6 | `updated_date` | `timestamp with time zone` | NO |  |
| 7 | `status` | `character varying` | NO |  |
| 8 | `bug_tracker` | `character varying` | NO |  |
| 9 | `owner_id` | `integer` | YES |  |
| 10 | `overlap` | `integer` | YES |  |
| 12 | `assignee_id` | `integer` | YES |  |
| 13 | `segment_size` | `integer` | NO |  |
| 18 | `project_id` | `integer` | YES |  |
| 19 | `data_id` | `integer` | YES |  |
| 20 | `dimension` | `character varying` | NO |  |
| 21 | `subset` | `character varying` | NO |  |
| 22 | `organization_id` | `integer` | YES |  |
| 23 | `source_storage_id` | `integer` | YES |  |
| 24 | `target_storage_id` | `integer` | YES |  |
| 25 | `assignee_updated_date` | `timestamp with time zone` | YES |  |
| 26 | `consensus_replicas` | `integer` | NO |  |
| 27 | `media_type` | `character varying` | NO |  |

### `engine_trackedshape`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `type` | `character varying` | NO |  |
| 2 | `occluded` | `boolean` | NO |  |
| 3 | `z_order` | `integer` | NO |  |
| 4 | `points` | `text` | NO |  |
| 5 | `id` | `bigint` | NO |  |
| 6 | `frame` | `integer` | NO |  |
| 7 | `outside` | `boolean` | NO |  |
| 8 | `track_id` | `bigint` | NO |  |
| 9 | `rotation` | `double precision` | NO |  |

### `engine_trackedshapeattributeval`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `value` | `character varying` | NO |  |
| 3 | `shape_id` | `bigint` | NO |  |
| 4 | `spec_id` | `integer` | NO |  |
| 5 | `job_id` | `integer` | NO |  |

### `engine_validationframe`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `path` | `character varying` | NO |  |
| 3 | `validation_params_id` | `integer` | NO |  |

### `engine_validationlayout`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `mode` | `character varying` | NO |  |
| 3 | `frames_per_job_count` | `integer` | YES |  |
| 4 | `frames` | `text` | NO |  |
| 5 | `disabled_frames` | `text` | NO |  |
| 6 | `task_data_id` | `integer` | NO |  |

### `engine_validationparams`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `mode` | `character varying` | NO |  |
| 3 | `frame_selection_method` | `character varying` | NO |  |
| 4 | `random_seed` | `integer` | YES |  |
| 5 | `frame_count` | `integer` | YES |  |
| 6 | `frame_share` | `double precision` | YES |  |
| 7 | `frames_per_job_count` | `integer` | YES |  |
| 8 | `frames_per_job_share` | `double precision` | YES |  |
| 9 | `task_data_id` | `integer` | NO |  |

### `engine_video`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `path` | `character varying` | NO |  |
| 3 | `height` | `integer` | NO |  |
| 4 | `width` | `integer` | NO |  |
| 5 | `data_id` | `integer` | YES |  |

### `growth_usergrowthdata`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `bigint` | NO |  |
| 2 | `github_prompt_shown_at` | `timestamp with time zone` | YES |  |
| 3 | `github_prompt_support_clicked` | `boolean` | NO |  |
| 4 | `promotion_notifications_allowed` | `boolean` | NO |  |
| 5 | `user_id` | `integer` | NO |  |

### `health_check_db_testmodel`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `title` | `character varying` | NO |  |

### `organizations_invitation`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `key` | `character varying` | NO |  |
| 2 | `created_date` | `timestamp with time zone` | NO |  |
| 3 | `membership_id` | `integer` | NO |  |
| 4 | `owner_id` | `integer` | YES |  |
| 5 | `sent_date` | `timestamp with time zone` | YES |  |

### `organizations_membership`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `is_active` | `boolean` | NO |  |
| 3 | `joined_date` | `timestamp with time zone` | YES |  |
| 4 | `role` | `character varying` | NO |  |
| 5 | `organization_id` | `integer` | NO |  |
| 6 | `user_id` | `integer` | YES |  |

### `organizations_organization`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `slug` | `character varying` | NO |  |
| 3 | `name` | `character varying` | NO |  |
| 4 | `description` | `text` | NO |  |
| 5 | `created_date` | `timestamp with time zone` | NO |  |
| 6 | `updated_date` | `timestamp with time zone` | NO |  |
| 7 | `contact` | `jsonb` | NO |  |
| 8 | `owner_id` | `integer` | YES |  |

### `quality_control_annotationconflict`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `frame` | `integer` | NO |  |
| 3 | `type` | `character varying` | NO |  |
| 4 | `severity` | `character varying` | NO |  |
| 5 | `report_id` | `integer` | NO |  |
| 6 | `attribute_names` | `jsonb` | NO |  |

### `quality_control_annotationid`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `obj_id` | `integer` | NO |  |
| 3 | `job_id` | `integer` | NO |  |
| 4 | `type` | `character varying` | NO |  |
| 5 | `shape_type` | `character varying` | YES |  |
| 6 | `conflict_id` | `integer` | NO |  |

### `quality_control_qualityreport`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `created_date` | `timestamp with time zone` | NO |  |
| 3 | `target_last_updated` | `timestamp with time zone` | NO |  |
| 4 | `gt_last_updated` | `timestamp with time zone` | YES |  |
| 5 | `data` | `jsonb` | NO |  |
| 6 | `job_id` | `integer` | YES |  |
| 8 | `task_id` | `integer` | YES |  |
| 9 | `assignee_id` | `integer` | YES |  |
| 10 | `assignee_last_updated` | `timestamp with time zone` | YES |  |
| 11 | `project_id` | `integer` | YES |  |

### `quality_control_qualityreport_parents`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `from_qualityreport_id` | `integer` | NO |  |
| 3 | `to_qualityreport_id` | `integer` | NO |  |

### `quality_control_qualityrequirement`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `created_date` | `timestamp with time zone` | NO |  |
| 3 | `updated_date` | `timestamp with time zone` | NO |  |
| 4 | `name` | `character varying` | NO |  |
| 5 | `annotation_type` | `character varying` | YES |  |
| 6 | `target_metric` | `character varying` | YES |  |
| 7 | `target_metric_threshold` | `double precision` | YES |  |
| 8 | `filter` | `text` | NO |  |
| 9 | `enabled` | `boolean` | NO |  |
| 10 | `sort_order` | `integer` | NO |  |
| 11 | `iou_threshold` | `double precision` | YES |  |
| 12 | `oks_sigma` | `double precision` | YES |  |
| 13 | `line_thickness` | `double precision` | YES |  |
| 14 | `point_size_base` | `character varying` | YES |  |
| 15 | `compare_line_orientation` | `boolean` | YES |  |
| 16 | `line_orientation_threshold` | `double precision` | YES |  |
| 17 | `compare_groups` | `boolean` | YES |  |
| 18 | `group_match_threshold` | `double precision` | YES |  |
| 19 | `check_covered_annotations` | `boolean` | YES |  |
| 20 | `object_visibility_threshold` | `double precision` | YES |  |
| 21 | `panoptic_comparison` | `boolean` | YES |  |
| 22 | `compare_attributes` | `boolean` | YES |  |
| 23 | `attribute_comparison` | `jsonb` | YES |  |
| 24 | `parent_id` | `integer` | YES |  |
| 25 | `settings_id` | `integer` | NO |  |

### `quality_control_qualitysettings`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 14 | `task_id` | `integer` | YES |  |
| 15 | `max_validations_per_job` | `integer` | NO |  |
| 20 | `created_date` | `timestamp with time zone` | NO |  |
| 21 | `updated_date` | `timestamp with time zone` | NO |  |
| 22 | `inherit` | `boolean` | NO |  |
| 23 | `project_id` | `integer` | YES |  |
| 24 | `job_filter` | `text` | NO |  |

### `rest_framework_api_key_apikey`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `character varying` | NO |  |
| 2 | `created` | `timestamp with time zone` | NO |  |
| 3 | `name` | `character varying` | NO |  |
| 4 | `revoked` | `boolean` | NO |  |
| 5 | `expiry_date` | `timestamp with time zone` | YES |  |
| 6 | `hashed_key` | `character varying` | NO |  |
| 7 | `prefix` | `character varying` | NO |  |

### `socialaccount_socialaccount`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `provider` | `character varying` | NO |  |
| 3 | `uid` | `character varying` | NO |  |
| 4 | `last_login` | `timestamp with time zone` | NO |  |
| 5 | `date_joined` | `timestamp with time zone` | NO |  |
| 6 | `extra_data` | `jsonb` | NO |  |
| 7 | `user_id` | `integer` | NO |  |

### `socialaccount_socialapp`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `provider` | `character varying` | NO |  |
| 3 | `name` | `character varying` | NO |  |
| 4 | `client_id` | `character varying` | NO |  |
| 5 | `secret` | `character varying` | NO |  |
| 6 | `key` | `character varying` | NO |  |
| 7 | `provider_id` | `character varying` | NO |  |
| 8 | `settings` | `jsonb` | NO |  |

### `socialaccount_socialapp_sites`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `socialapp_id` | `integer` | NO |  |
| 3 | `site_id` | `integer` | NO |  |

### `socialaccount_socialtoken`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `token` | `text` | NO |  |
| 3 | `token_secret` | `text` | NO |  |
| 4 | `expires_at` | `timestamp with time zone` | YES |  |
| 5 | `account_id` | `integer` | NO |  |
| 6 | `app_id` | `integer` | YES |  |

### `webhooks_webhook`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `target_url` | `character varying` | NO |  |
| 3 | `description` | `character varying` | NO |  |
| 4 | `events` | `character varying` | NO |  |
| 5 | `type` | `character varying` | NO |  |
| 6 | `content_type` | `character varying` | NO |  |
| 7 | `secret` | `character varying` | NO |  |
| 8 | `is_active` | `boolean` | NO |  |
| 9 | `enable_ssl` | `boolean` | NO |  |
| 10 | `created_date` | `timestamp with time zone` | NO |  |
| 11 | `updated_date` | `timestamp with time zone` | NO |  |
| 12 | `organization_id` | `integer` | YES |  |
| 13 | `owner_id` | `integer` | YES |  |
| 14 | `project_id` | `integer` | YES |  |

### `webhooks_webhookdelivery`

| ลำดับ | คอลัมน์ | ชนิดข้อมูล | Nullable | Default |
|---:|---|---|:---:|---|
| 1 | `id` | `integer` | NO |  |
| 2 | `event` | `character varying` | NO |  |
| 3 | `status_code` | `integer` | YES |  |
| 4 | `redelivery` | `boolean` | NO |  |
| 5 | `created_date` | `timestamp with time zone` | NO |  |
| 6 | `updated_date` | `timestamp with time zone` | NO |  |
| 7 | `changed_fields` | `character varying` | NO |  |
| 8 | `request` | `jsonb` | NO |  |
| 9 | `response` | `jsonb` | NO |  |
| 10 | `webhook_id` | `integer` | NO |  |
| 11 | `attempt` | `integer` | YES |  |

## ตารางสำคัญสำหรับ workflow

| หน้าที่ | ตารางหลัก | ความสัมพันธ์สำคัญ |
|---|---|---|
| ผู้ใช้ | `auth_user` | งานและองค์กรอ้างอิง `user_id` หรือ `assignee_id` |
| Organization | `organizations_organization` | งานอ้างอิงด้วย `organization_id` |
| สมาชิกองค์กร | `organizations_membership` | เชื่อม user กับ organization และเก็บ role |
| Project | `engine_project` | Project มีหลาย Task |
| Task | `engine_task` | เชื่อม Project, Data, Organization |
| Job | `engine_job` | เชื่อม Segment และผู้รับผิดชอบ; ดู stage/state/status |
| Segment | `engine_segment` | แบ่งช่วงเฟรมของ Task และสร้าง Job |
| Issue | `engine_issue` | ผูกกับ Job และมีสถานะ resolved |
| Comment | `engine_comment` | ผูกกับ Issue |
| Labels | `engine_label` | label ของ Task/Project |
| Annotation | `engine_labeledshape`, `engine_labeledimage`, `engine_labeledtrack` | ผูกกับ Job และ Label |
| Quality Control | `quality_control_qualityreport`, `quality_control_annotationconflict` | ผลตรวจและ conflict |

## คำสั่งดู schema แบบเจาะจง

```bash
# ดูคอลัมน์, index และ foreign key
docker compose exec -T cvat_db psql -U root -d cvat -c '\\d+ engine_job'

# ดู foreign key ทุกตาราง
 docker compose exec -T cvat_db psql -U root -d cvat -c "SELECT tc.table_name,kcu.column_name,ccu.table_name AS referenced_table,ccu.column_name AS referenced_column FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name=kcu.constraint_name AND tc.table_schema=kcu.table_schema JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name=tc.constraint_name AND ccu.table_schema=tc.table_schema WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema='public' ORDER BY tc.table_name;"
```

## หมายเหตุ

- ตาราง annotation มีทั้ง shape, image, track และ attribute จึงไม่ควรอ่านเพียงตารางเดียวเพื่อสรุป annotation ทั้งหมด
- ค่า `points` และฟิลด์ JSON/text บางส่วนเป็น representation ภายใน CVAT ควรใช้ API หรือ export format สำหรับงาน downstream
- schema อาจเปลี่ยนตาม version และ migration ของ CVAT ควร regenerate เอกสารหลัง upgrade


