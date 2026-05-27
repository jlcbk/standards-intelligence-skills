# GB Vehicle Safety Demo

This demo exercises the first vertical workflow for the skills pack:

```text
source-intake -> provision-compiler -> regulatory-answer -> coverage report
```

The demo uses two official source metadata records:

- GB 7258-2017, `机动车运行安全技术条件`
- GB 1589-2016, `汽车、挂车及汽车列车外廓尺寸、轴荷及质量限值`

The official metadata comes from the national standards public service platform:

- <https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D81CEDD3A7E05397BE0A0AB82A>
- <https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8118AD3A7E05397BE0A0AB82A>

## Boundary

This package intentionally does **not** store the PDF files or long verbatim
standard text. The provisions and answer packets are synthetic/paraphrased demo
artifacts that test repository workflow and schema shape. They are not
authoritative compliance content.

Use this package for:

- testing skill selection;
- testing JSON/JSONL artifact validation;
- demonstrating citation-shaped answer packets;
- proving that public metadata plus private/BYOD text can coexist safely.

Do not use this package for:

- legal advice;
- vehicle compliance decisions;
- certification conclusions;
- claiming exact GB 7258 or GB 1589 requirements.
