# ICPC resolver eventfeed converter(For nowcoder contest)

本脚本主要用于根据牛客的提交记录和队伍名单等信息生成符合CCS标准的eventfeed文件(NODE Json)。生成的文件可以使用ICPC Tools中的Award进行颁奖，并使用Resolver进行滚榜。

暂时未支持校徽和队伍照片。如果您非常熟悉如何使用eventfeed.json进行本地cdp滚榜，欢迎对本项目进行修改！

## Configuration for contest information file directory

首先你需要对各个必须文件的目录进行配置，如果没有特殊需求，可以直接使用 `./tool_config.yaml`下的默认配置。

以下为各个配置项的解释：

* `contest_config`：存放比赛基本信息配置文件的路径
* `problem_config`：存放比赛题目配置文件的路径
* `status_confug`：存放比赛状态更新信息的路径(后面将移除该文件)
* `groups_confug`：存放比赛用户组配置文件的路径
* `organizations_info`：存放参赛机构/组织/学校的信息文件路径
* `teams_info`：存放参赛队伍信息的CSV文件路径
* `submissions_info`：存放提交信息的CSV文件路径

## part submission and judgement

submission和judgement部分采用的是导出牛客xls文件后，数值处理成整型，时间处理成格式r"%Y-%m-%d %H:%M:%S"，并转换成csv格式放置路径上。
如测试文件所示。

~~请注意，本代码中需要手动修改比赛开始时间，请务必记得修改~~
