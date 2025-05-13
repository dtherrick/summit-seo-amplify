tests/api/v1/test_users.py:3:2: F821 Undefined name `pytest`
  |
1 | from fastapi import status
2 |
3 | @pytest.mark.asyncio
  |  ^^^^^^ F821
4 | async def test_update_user_me_validation_invalid_type(
5 |     client, mock_dynamodb, mock_get_current_user
  |

tests/api/v1/test_users.py:17:2: F821 Undefined name `pytest`
   |
15 |     mock_dynamodb.update_item.assert_not_called()
16 |
17 | @pytest.mark.asyncio
   |  ^^^^^^ F821
18 | async def test_update_user_me_validation_empty_payload(
19 |     client, mock_dynamodb, mock_get_current_user
   |

tests/api/v1/test_users.py:32:2: F821 Undefined name `pytest`
   |
30 |     mock_dynamodb.update_item.assert_not_called()
31 |
32 | @pytest.mark.asyncio
   |  ^^^^^^ F821
33 | async def test_update_user_me_validation_extra_field(
34 |     client, mock_dynamodb, mock_get_current_user, test_user_data
   |

Found 3 errors.
Error: Process completed with exit code 1.