"""
Wsgirouter3 extension for pdf generation using weasyprint.

Homepage: https://github.com/andruskutt/wsgirouter3-weasyprint

License: MIT
"""

import functools
from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping, NoReturn, Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    import ssl

from weasyprint import HTML  # type: ignore

__all__ = ['Pdf', 'PdfConfig', 'install']

_NO_KWARGS: Dict[str, Any] = {}


@dataclass
class PdfConfig:
    html_generator: Callable[[str, Any], str]
    url_fetcher: Optional[Callable[[str, int, Any], Dict[str, Any]]] = None
    default_headers: Optional[Mapping[str, str]] = None


@dataclass
class Pdf:
    html_id: str
    context: Any = None
    write_pdf_kwargs: Optional[Mapping[str, Any]] = None
    headers: Optional[Mapping[str, str]] = None

    def write_pdf_with(self, **kwargs: Any) -> 'Pdf':
        self.write_pdf_kwargs = kwargs
        return self


def _disable_url_fetching(url: str, timeout: int = 10, ssl_context: 'Optional[ssl.SSLContext]' = None) -> NoReturn:
    raise NotImplementedError('Url fetching is disabled')


def pdf_generator(config: PdfConfig, pdf: Pdf, headers: Dict[str, str]) -> Tuple[bytes]:
    html = config.html_generator(pdf.html_id, pdf.context)
    url_fetcher = config.url_fetcher or _disable_url_fetching
    response = HTML(string=html, url_fetcher=url_fetcher).write_pdf(**(pdf.write_pdf_kwargs or _NO_KWARGS))

    headers['Content-Type'] = 'application/pdf'
    headers['Content-Length'] = str(len(response))

    if config.default_headers:
        headers.update(config.default_headers)
    if pdf.headers:
        headers.update(pdf.headers)

    return (response,)


def install(wsgirouter3: Any, config: PdfConfig) -> None:
    wsgirouter3.config.result_converters.append((
        lambda result: isinstance(result, Pdf),
        functools.partial(pdf_generator, config)
    ))
