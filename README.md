<p align="center">
  <a href="https://github.com/AlexDemure/gadfasthealth">
    <a href="https://ibb.co/xK8Cydh3"><img src="https://i.ibb.co/Y4TR6w2b/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  FastAPI health check extension for Kubernetes liveness, readiness, and startup probes
</p>

---

### Installation

```
pip install gadfasthealth
```

### Usage

```python
def check_redis() -> bool:
    return False

async def check_db() -> bool:
    return True

app = fastapi.FastAPI()

health = Health(
    ("/-/liveness", check_db),
    ("/-/readiness", check_db, check_redis),
    ("/-/startup", check_db),
    ("/-/custom"),
)

app.include_router(health.router)
```
