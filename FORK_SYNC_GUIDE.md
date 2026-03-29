# Fork Sync Strategy

## 📋 Repository Structure

- **主项目（上游）**: `https://github.com/abhi1693/openclaw-mission-control.git`
- **你的项目（origin）**: `https://github.com/sxyseo/openclaw-mission-control.git`

## 🔄 Git Remote 配置

```bash
# 查看当前的 remote 配置
git remote -v

# 应该看到：
# origin    https://github.com/abhi1693/openclaw-mission-control.git (fetch)
# origin    https://github.com/abhi1693/openclaw-mission-control.git (push)
# myfork    https://github.com/sxyseo/openclaw-mission-control.git (fetch)
# myfork    https://github.com/sxyseo/openclaw-mission-control.git (push)
```

## 📝 工作流程

### 1️⃣ 开发新功能

```bash
# 从 master 创建功能分支
git checkout master
git pull origin master  # 先同步上游最新代码
git checkout -b feature/your-feature-name

# 进行开发...
# git add .
# git commit -m "feat: your feature description"

# 推送到你的 fork
git push myfork feature/your-feature-name

# 合并到你的 master
git checkout master
git merge feature/your-feature-name
git push myfork master
```

### 2️⃣ 同步上游新功能

```bash
# 确保在 master 分支
git checkout master

# 拉取上游最新代码
git pull origin master

# 如果有冲突，解决冲突后：
# git add .
# git commit -m "chore: resolve merge conflicts with upstream"

# 推送到你的 fork
git push myfork master
```

### 3️⃣ 保留你的新功能同时同步上游

**情况：上游有新功能，你也有新功能，需要合并**

```bash
# 1. 确保你的功能分支是最新的
git checkout feature/your-feature-name
git merge master  # 合和你 fork 的最新 master

# 2. 切换到 master 并同步上游
git checkout master
git pull origin master  # 这会带来上游的新功能

# 3. 将你的功能合并到包含上游新功能的 master
git merge feature/your-feature-name
# 如果有冲突，手动解决

# 4. 推送更新后的 master 到你的 fork
git push myfork master
```

## 🚨 冲突解决

当同步上游时遇到冲突：

```bash
# 1. 尝试合并时如果遇到冲突
git pull origin master
# CONFLICT (content): Merge conflict in frontend/src/app/layout.tsx

# 2. 查看冲突文件
git status

# 3. 手动解决冲突（在文件中标记为 <<<<<<< ======= >>>>>>> 的部分）

# 4. 标记冲突已解决
git add frontend/src/app/layout.tsx

# 5. 完成合并
git commit -m "chore: resolve merge conflicts with upstream updates"

# 6. 推送更新
git push myfork master
```

## 🔄 定期同步建议

**建议每次开发前先同步上游**：

```bash
# 开发新功能前的标准流程
git checkout master
git pull origin master        # 同步上游最新代码
git checkout -b feature/new-feature
# ... 进行开发 ...
git push myfork feature/new-feature
```

## 📊 分支策略图

```
主项目 (origin/master)
    ↓ 拉取更新
你的 fork (myfork/master)
    ↓ 创建功能分支
功能分支 (feature/your-feature)
    ↓ 开发完成后
你的 fork (myfork/master) ← 最终发布版本
```

## 🎯 最佳实践

1. **定期同步**: 每次开发前先 `git pull origin master`
2. **功能分支**: 新功能都在独立分支开发
3. **小步提交**: 频繁提交，便于合并和冲突解决
4. **测试后合并**: 确保功能正常后再合并到 master
5. **保持清洁**: 删除已合并的功能分支

## 🔧 实用命令

```bash
# 查看当前分支
git branch

# 查看所有分支（包括远程）
git branch -a

# 查看最近的提交
git log --oneline --graph --all

# 查看差异
git diff origin/master

# 放弃本地更改（慎用）
git reset --hard origin/master
```

## 📱 当前项目状态

- ✅ **i18n 功能**: 已合并到 `myfork/master`
- ✅ **上游同步**: 已同步到最新 commit (94a7da4)
- ✅ **功能完整**: 包含完整的国际化支持

## 🚀 部署命令

```bash
# 确保在 master 分支
git checkout master
git pull origin master  # 先同步上游
git pull myfork master   # 再同步你的 fork
git push myfork master   # 推送最新版本

# 启动服务
make run
```
