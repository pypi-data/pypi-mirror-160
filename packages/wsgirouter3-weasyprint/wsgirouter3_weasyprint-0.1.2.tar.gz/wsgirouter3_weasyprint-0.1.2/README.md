# [Weasyprint](https://weasyprint.org/) plugin for [wsgirouter3](https://github.com/andruskutt/wsgirouter3)

## Usage

Configure application to use plugin

```python
def _generator(html_id: str, context: Any) -> str:
    # your choice of template engine


application = wsgirouter3.WsgiApp(router)
wsgirouter3_weasyprint.install(
    application,
    wsgirouter3_weasyprint.PdfConfig(html_generator=_generator)
)
```

Return instance of Pdf from endpoint

```python
@router.get('/get', produces='application/pdf')
def get() -> Pdf:
    html_generation_ctx = {'context': 'variable'}
    return Pdf('html_template_id', html_generation_ctx)
```

## Installation

```shell
$ pip install wsgirouter3_weasyprint
```
