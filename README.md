# VehAutoTool

整车调试工具——CAN 报文解析与可视化的初始版本。

## 功能概览
- **多格式解析**：支持常见的 `candump`、`CANID#DATA` 以及 JSON 行格式。
- **可视化**：可选用 Matplotlib 将指定字节的变化趋势绘制为折线图。
- **数据导出**：将解析结果导出为 JSON，便于后续分析或接入其他系统。
- **AI 接口预留**：`AIInsights` 提供了摘要能力，后续可接入大模型进行故障诊断、模式识别等高级分析。

## 使用方式
1. 安装依赖（可选，若需要绘图）：
   ```bash
   pip install matplotlib
   ```

2. 运行 CLI（项目自带 `samples/sample.log` 示例）：
   ```bash
   python -m vehautotool.cli samples/sample.log --export parsed.json --plot-byte 0 --summary
   ```

   - `log`：待解析的日志文件路径。
   - `--export`：将解析的 CAN 帧写入 JSON。
   - `--plot-byte`：指定要可视化的字节索引（0 起始）。
   - `--plot-output`：图像保存路径，默认为 `can_byte_series.png`。
   - `--summary`：输出基于 AI 接口预留的摘要信息。

## 支持的日志示例
- candump 样式：`(1606406475.123456) can0 123#11223344`
- can-utils 样式：`123#11223344` 或 `1606406475.123456 123#11223344`
- JSON 行：`{"can_id": "0x123", "data": "11223344", "timestamp": 1606406475.123456}`

## 后续规划
- 在线报文采集与实时分析。
- 更丰富的协议描述与信号定义支持（DBC/Arxml）。
- 接入 AI 模型，提供故障根因分析与自学习能力。
