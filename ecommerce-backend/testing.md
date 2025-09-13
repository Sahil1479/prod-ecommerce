## API Testing

---

### 1. User Registration

* Method: `POST`
* URL: `http://127.0.0.1:8000/api/v1/users/register/`
* Body → raw → JSON:

  ```json
  {
    "username": "sahil123",
    "email": "sahil@example.com",
    "password": "securepass123",
    "role": "customer"
  }
  ```

---

* Expected Response

```json
{
  "id": 1,
  "username": "sahil123",
  "email": "sahil@example.com",
  "role": "customer"
}
```

👉 Notice that the `password` will not be returned — this is intentional for security.

---