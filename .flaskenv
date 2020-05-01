FLASK_APP=runapp.py
FLASK_ENV=development


# Database URIs
DEV_DATABASE_URL="postgresql://postgres:abdou@127.0.0.1:5432/eval_project"
TEST_DATABASE_URL="postgresql://postgres:abdou@127.0.0.1:5432/eval_project_test"
DATABASE_URL="postgresql://postgres:abdou@127.0.0.1:5432/eval_project"


# The default API base path (used by the frontend)
ENDPOINTS_BASE_URL="http://127.0.0.1:5000/api/v1"


# Auth0 - config
# Tenant
AUTH0_DOMAIN="manianis.eu.auth0.com"

# Create an application in Auth0
AUTH0_CLIENT_ID="KbyHBjGopjc64xpW20Lta7bO3ZGQKsDi"
AUTH0_CLIENT_SECRET="fTVUsEn3plM0YipH7ncfqYots7KsYE6ZaPmrtxXM7gJimynVcZMJeYaW1iOLHeMb"
AUTH0_CALLBACK_URI="http://127.0.0.1:5000/callback"

# Create an API for that application
AUTH0_APP_AUDIENCE="manianis.evalappproject.api"

# The API management key is used to affect roles to the newly signed-up users
AUTH0_API_MANAGEMENT="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkwVzVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJadXpGWU5qZlNnQk1rQ3V6dEo3UWc0MHhTNW9ZM0Y1UUBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9tYW5pYW5pcy5ldS5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTU4Nzg4ODQ1MywiZXhwIjoxNTg4NDkzMjUwLCJhenAiOiJadXpGWU5qZlNnQk1rQ3V6dEo3UWc0MHhTNW9ZM0Y1USIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgcmVhZDp1c2VyX2N1c3RvbV9ibG9ja3MgY3JlYXRlOnVzZXJfY3VzdG9tX2Jsb2NrcyBkZWxldGU6dXNlcl9jdXN0b21fYmxvY2tzIGNyZWF0ZTp1c2VyX3RpY2tldHMgcmVhZDpjbGllbnRzIHVwZGF0ZTpjbGllbnRzIGRlbGV0ZTpjbGllbnRzIGNyZWF0ZTpjbGllbnRzIHJlYWQ6Y2xpZW50X2tleXMgdXBkYXRlOmNsaWVudF9rZXlzIGRlbGV0ZTpjbGllbnRfa2V5cyBjcmVhdGU6Y2xpZW50X2tleXMgcmVhZDpjb25uZWN0aW9ucyB1cGRhdGU6Y29ubmVjdGlvbnMgZGVsZXRlOmNvbm5lY3Rpb25zIGNyZWF0ZTpjb25uZWN0aW9ucyByZWFkOnJlc291cmNlX3NlcnZlcnMgdXBkYXRlOnJlc291cmNlX3NlcnZlcnMgZGVsZXRlOnJlc291cmNlX3NlcnZlcnMgY3JlYXRlOnJlc291cmNlX3NlcnZlcnMgcmVhZDpkZXZpY2VfY3JlZGVudGlhbHMgdXBkYXRlOmRldmljZV9jcmVkZW50aWFscyBkZWxldGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGNyZWF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgcmVhZDpydWxlcyB1cGRhdGU6cnVsZXMgZGVsZXRlOnJ1bGVzIGNyZWF0ZTpydWxlcyByZWFkOnJ1bGVzX2NvbmZpZ3MgdXBkYXRlOnJ1bGVzX2NvbmZpZ3MgZGVsZXRlOnJ1bGVzX2NvbmZpZ3MgcmVhZDpob29rcyB1cGRhdGU6aG9va3MgZGVsZXRlOmhvb2tzIGNyZWF0ZTpob29rcyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgdXBkYXRlOmN1c3RvbV9kb21haW5zIHJlYWQ6ZW1haWxfdGVtcGxhdGVzIGNyZWF0ZTplbWFpbF90ZW1wbGF0ZXMgdXBkYXRlOmVtYWlsX3RlbXBsYXRlcyByZWFkOm1mYV9wb2xpY2llcyB1cGRhdGU6bWZhX3BvbGljaWVzIHJlYWQ6cm9sZXMgY3JlYXRlOnJvbGVzIGRlbGV0ZTpyb2xlcyB1cGRhdGU6cm9sZXMgcmVhZDpwcm9tcHRzIHVwZGF0ZTpwcm9tcHRzIHJlYWQ6YnJhbmRpbmcgdXBkYXRlOmJyYW5kaW5nIHJlYWQ6bG9nX3N0cmVhbXMgY3JlYXRlOmxvZ19zdHJlYW1zIGRlbGV0ZTpsb2dfc3RyZWFtcyB1cGRhdGU6bG9nX3N0cmVhbXMgY3JlYXRlOnNpZ25pbmdfa2V5cyByZWFkOnNpZ25pbmdfa2V5cyB1cGRhdGU6c2lnbmluZ19rZXlzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.n7_-VR1f48xW8k-y7ftuxR86g4uYKVBx2bLvDnUb4qD2cOiXCGOLL-Crt8MQfs9gj6FcnCfBKNKeJAud5xoc_JnFFd6YbTYTe4o5ScoVnf6Ntzp-b_GmjBX5a8BAtGuU7ZEt3AikwbqOpicONoBRaMIf--DMzDoB_FrlS6UVP7584-xbBghCnHcZW4nRtgrVWAu7cP7RRGXFKnZhox269_7CVcAetoq3GBR5tB7r-Lu8WqXwcesf6Akzvp1GvTtFJnjkzup0mmYMkUvPvfNMLWBbC8TIDq8vYLo_uFUWqxMQAZ6brp21J_gLctFwcWAvCpxxbnDJq8Fl-auolJog_w"

# Used in testing - no need to change this vars
AUTH0_CLIENT_ID1="V8IAqOYFsq8vzjF5isGSSJjokelaSMrJ"
AUTH0_CLIENT_SECRET1="Q1sbUQCy7wzOzJVZCmvh-n-p1y7X6Rw3ijtQvk1e7K7hUSpBbOx2oFqdR9klPQK-"

AUTH0_CLIENT_ID2="ktajodbWnCgRYZBZJUGNiknBSYcNui32"
AUTH0_CLIENT_SECRET2="Ygr75RtK_6Vkf2KizMmrK0fo0T3nbe2C6qjlzzBCWxis81IpJGMFfRMKLOeOPzy3"
