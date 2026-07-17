# `hasattr` and `getattr` — quick reference

Both work on **any Python object** (not just `self` in a class) — they check/read attributes by name.

## `hasattr(obj, name)` → bool

"Does `obj` have an attribute called `name`?"

```python
hasattr(self, 'image_a')   # True if self.image_a has been set, else False
```

Equivalent to (but cleaner than):
```python
try:
    self.image_a
    exists = True
except AttributeError:
    exists = False
```

### Real usage pattern: lazy caching
From `qc_tissue_fold_lost_tma.py`'s `_load_round`:
```python
def _load_round(self, round_num: int):
    if not hasattr(self, 'image_a'):
        self.image_a = self._load_image(1)          # only runs once
        self._thr_a = filters.threshold_otsu(self.image_a)

    if getattr(self, 'round_num', None) != round_num:
        self.image_b = self._load_image(round_num)  # only reloads if round changed
        self.round_num = round_num
```
`image_a` doesn't exist yet the *first* time this method runs (it's not set in `__init__`). `hasattr` lets you ask "has this been computed before?" without crashing — if not, compute and store it; if yes, skip and reuse what's cached.

---

## `getattr(obj, name, default)` → value

"Give me `obj.name`, or `default` if it doesn't exist."

```python
getattr(self, 'round_num', None)   # returns self.round_num if set, else None
```

Equivalent to:
```python
self.round_num if hasattr(self, 'round_num') else None
```

`getattr` is really just `hasattr` + fetching the value, combined into one call — use it when you want the *value* (with a safe fallback), use `hasattr` when you only want a yes/no.

### Real usage pattern: "did this change since last time?"
```python
if getattr(self, 'round_num', None) != round_num:
    ...  # round_num either doesn't exist yet (first call) or is a different round
```
This safely compares against a possibly-not-yet-set attribute — no `AttributeError` on the very first call, no need for a separate `hasattr` check first.

---

## Related: `setattr(obj, name, value)`

Sets an attribute by string name instead of `obj.name = value` directly. Less commonly needed day-to-day, but completes the set — useful when the attribute name itself is a variable, not known until runtime:
```python
setattr(self, f'round_{i}', image)   # same as self.round_3 = image, if i == 3
```

---

## When to reach for these vs. just using `self.x` directly

- If an attribute is **always** set in `__init__`, just use `self.x` normally — no need for `hasattr`/`getattr`.
- Reach for `hasattr`/`getattr` specifically when an attribute is set **lazily** (only after some method runs) and other code might run before or after that point — i.e. you genuinely don't know if it exists yet.

See [[median_mad_robust_thresholding_explainer]] for the QC pipeline this pattern is used in.
