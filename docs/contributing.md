---
title: 贡献指南
description: 用可追溯证据、双语一致性和可复现审查共同维护电子工程学习导航。
---


# 贡献入口

发现一个错误，不需要先学会整套数据管线；准备新增课程，也不应从手改生成页面开始。按改动大小选择下面一条路径。

## 路径一：快速更正

适合失效链接、先修错误、翻译偏差、版本变化或安全问题：

- [报告失效或受限链接](https://github.com/appleweiping/eediy/issues/new?template=broken-link.yml)
- [提交事实或安全更正](https://github.com/appleweiping/eediy/issues/new?template=content-error.yml)
- [补充学习经历或课程变化](https://github.com/appleweiping/eediy/issues/new?template=course-feedback.yml)
- [先在 Discussions 讨论范围](https://github.com/appleweiping/eediy/discussions)

给出具体页面、需要修改的句子、一手来源和核验日期即可。事实或安全问题可以先做最小修正，不必等待整页重写。

## 路径二：新增课程、项目或完整改稿

- [提出课程推荐](https://github.com/appleweiping/eediy/issues/new?template=course.yml)
- [提出项目或实验方案](https://github.com/appleweiping/eediy/issues/new?template=project.yml)
- [查看或发起 Pull Request](https://github.com/appleweiping/eediy/compare)
- [阅读仓库贡献说明](https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md)

先用 Issue 确认课程是否重复、方向与范围是否合适；准备好双语内容和可追溯证据后，再提交 Pull Request。

## 改对文件

课程页和路线页由权威数据生成，不能直接修改 `docs/courses/`、`docs/en/courses/`、`docs/routes/` 或 `docs/en/routes/`。

| 要修改的内容 | 权威入口 |
| --- | --- |
| 课程身份、学校、课号、方向与先修 | [`data/course_candidates.json`](https://github.com/appleweiping/eediy/blob/main/data/course_candidates.json) |
| 官方资源、开放状态和核验记录 | [`data/course_resources.json`](https://github.com/appleweiping/eediy/blob/main/data/course_resources.json) |
| 课程角色与编辑判断 | [`data/course_editorial.json`](https://github.com/appleweiping/eediy/blob/main/data/course_editorial.json) |
| 导读状态、来源清单和双语片段位置 | [`data/course_guides.json`](https://github.com/appleweiping/eediy/blob/main/data/course_guides.json) |
| 单课导读正文 | [`content/course-guides/`](https://github.com/appleweiping/eediy/tree/main/content/course-guides) |
| 方向比较正文 | [`content/track-guides/`](https://github.com/appleweiping/eediy/tree/main/content/track-guides) |
| 路线阶段与依赖 | [`data/routes.json`](https://github.com/appleweiping/eediy/blob/main/data/routes.json) |

如果拿不准一项事实属于哪一层，先看[完整数据流与生成顺序](https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md#authoritative-data-flow--权威数据流)。

## 一次可评审的贡献需要什么

- 重要事实回到课程、机构、教师、制造商或标准组织的一手页面，并记录核验日期。
- 明确讲义、作业、答案、实验、代码和考试分别是否公开；不要用“资源齐全”代替检查。
- 写清登录、付费、地区、许可证、指定硬件和实验条件。
- 中英文的事实、数字、链接、风险与推荐保持一致，句子可以按各自语言自然表达。
- 只有提供完成范围、环境、实际投入、卡点和可检查产物时，才把内容写成学习者经验。
- 涉及电气、激光、射频、电池、化学或机械风险时，引用正式安全来源；不提供绕过联锁、保护或监督的做法。

## 收录标准：先闭合一个模块，不追求目录数字

一个方向优先形成一个可学习闭环：**一门主线课、一个确有证据的中文替代、一套练习或实验、一个官方参考入口，以及一个能验证学习结果的任务**。某项暂时找不到，就公开写成缺口；不要为了凑课程、页面、链接或项目数量加入重复、低证据材料。

查找新资源时按以下顺序判断：

1. 大学或教师发布的完整开放课程；
2. 政府、标准组织和开源项目的官方文档；
3. 芯片、EDA 与仪器厂商的正式培训和应用资料；
4. 有明确作者、可检查练习或自动反馈的学习站；
5. 社区文章只补一个具体缺口，不承担主线事实。

新增条目至少要回答：它替代或补充哪一项、官方材料实际开放到哪里、需要什么先修和设备、学习者最后留下什么证据。若原条目失去官方入口、内容被更完整资源取代，或只剩无法核实的宣传，应降级、归档或删除；历史数量不是保留理由。

不得上传付费答案、受限课件、PDK 或厂商保密资料，也不得提交密钥、个人数据和未经许可的图片。利益相关关系应在变更说明中披露。第三方材料边界见[许可与引用](about/license.md)。

## 本地预览与检查

```bash
python -m pip install --require-hashes -r requirements.lock
python -m mkdocs serve
python scripts/run_quality.py
```

修改权威课程数据时，还需按[仓库贡献说明](https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md)中的顺序重新生成页面。提交前实际阅读中英文页面，并在 Pull Request 中列出改动、来源、仍不确定的部分和已运行的检查。
