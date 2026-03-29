#!/bin/bash
# Mission Control 自动化配置脚本 (Bash版本)
# 参照 gstack 理念，一键创建完整的 AI 项目管理环境

API_BASE="http://localhost:8000"
AUTH_TOKEN="640d5d3e5e5e5010f8e318489aa88de4bbd111e244a00af17dc0a86eba53b811ab"

echo "🚀 Mission Control 自动化配置开始..."
echo "============================================================"

# 检查服务是否运行
echo "🔍 检查服务状态..."
if ! curl -s "$API_BASE/healthz" > /dev/null; then
    echo "❌ 后端服务未运行，请先启动服务: make run"
    exit 1
fi
echo "✅ 后端服务运行正常"

# 创建配置函数
create_board_group() {
    local name="$1"
    local description="$2"

    echo "📊 创建 Board Group: $name"
    response=$(curl -s -X POST "$API_BASE/api/v1/board-groups" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$name\", \"description\": \"$description\"}")

    if echo "$response" | grep -q '"id"'; then
        local id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        echo "✅ Board Group 创建成功: $name (ID: $id)"
        echo "$id"
    else
        echo "❌ Board Group 创建失败: $name"
        echo "$response"
        return 1
    fi
}

create_board() {
    local name="$1"
    local description="$2"
    local gateway_id="$3"
    local group_id="$4"

    echo "📋 创建 Board: $name"

    # 简化的 slug 生成
    local slug=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]+/-/g' | sed 's/^-\|-$//g')

    local json_data="{\"name\": \"$name\", \"slug\": \"$slug\", \"description\": \"$description\", \"gateway_id\": \"$gateway_id\""

    if [ -n "$group_id" ]; then
        json_data="$json_data, \"board_group_id\": \"$group_id\""
    fi

    json_data="$json_data}"

    response=$(curl -s -X POST "$API_BASE/api/v1/boards" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$json_data")

    if echo "$response" | grep -q '"id"'; then
        local id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        echo "✅ Board 创建成功: $name (ID: $id)"
        echo "$id"
    else
        echo "❌ Board 创建失败: $name"
        echo "$response"
        return 1
    fi
}

create_agent() {
    local name="$1"
    local board_id="$2"
    local description="$3"

    echo "🤖 创建 Agent: $name"

    # 简化的 slug 生成
    local slug=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]+/-/g' | sed 's/^-\|-$//g')

    response=$(curl -s -X POST "$API_BASE/api/v1/agents" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$name\", \"slug\": \"$slug\", \"description\": \"$description\", \"board_id\": \"$board_id\", \"status\": \"online\"}")

    if echo "$response" | grep -q '"id"'; then
        local id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        echo "✅ Agent 创建成功: $name (ID: $id)"
        echo "$id"
    else
        echo "❌ Agent 创建失败: $name"
        echo "$response"
        return 1
    fi
}

# 主配置流程
main() {
    # 检查是否有现有 Gateway
    echo ""
    echo "📡 第一步：配置 Gateway"
    echo "----------------------------------------"

    gateway_response=$(curl -s "$API_BASE/api/v1/gateways" \
        -H "Authorization: Bearer $AUTH_TOKEN")

    if echo "$gateway_response" | grep -q '"items"'; then
        gateway_count=$(echo "$gateway_response" | grep -o '"count":[0-9]*' | cut -d':' -f2)
        if [ "$gateway_count" -gt 0 ]; then
            gateway_id=$(echo "$gateway_response" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
            echo "✅ 使用现有 Gateway (ID: $gateway_id)"
        else
            echo "❌ 没有找到 Gateway，请手动创建"
            exit 1
        fi
    else
        echo "❌ 无法访问 Gateway API"
        exit 1
    fi

    # 创建 Board Groups
    echo ""
    echo "📊 第二步：创建 Board Groups"
    echo "----------------------------------------"

    group_personal=$(create_board_group "Personal Projects" "管理个人开发项目和学习任务")
    group_work=$(create_board_group "Work Projects" "处理工作相关的开发和维护")
    group_learning=$(create_board_group "Learning & Skills" "技术学习和能力提升")
    group_tools=$(create_board_group "Tools & Utilities" "开发实用工具和脚本")
    group_research=$(create_board_group "R&D Experiments" "新技术研究和实验项目")

    # 创建 Boards
    echo ""
    echo "📋 第三步：创建专家 Boards"
    echo "----------------------------------------"

    board_frontend=$(create_board "Frontend Development" "前端开发和UI/UX设计" "$gateway_id" "$group_personal")
    board_backend=$(create_board "Backend Development" "后端API和数据库设计" "$gateway_id" "$group_personal")
    board_fullstack=$(create_board "Full Stack Projects" "全栈开发项目" "$gateway_id" "$group_personal")
    board_learning=$(create_board "Tech Learning Path" "技术学习路径" "$gateway_id" "$group_learning")
    board_docs=$(create_board "Documentation Hub" "技术文档中心" "$gateway_id" "$group_learning")

    # 创建 Agents
    echo ""
    echo "🤖 第四步：创建专家 Agents"
    echo "----------------------------------------"

    agent_frontend=$(create_agent "Frontend Expert" "$board_frontend" "前端开发专家 - React、Vue、Angular")
    agent_backend=$(create_agent "Backend Expert" "$board_backend" "后端开发专家 - API设计、数据库")
    agent_fullstack=$(create_agent "Full Stack Developer" "$board_fullstack" "全栈开发工程师")
    agent_learning=$(create_agent "Learning Coach" "$board_learning" "学习教练")
    agent_writer=$(create_agent "Technical Writer" "$board_docs" "技术文档专家")

    # 总结
    echo ""
    echo "============================================================"
    echo "🎉 自动化配置完成！"
    echo "============================================================"
    echo "📊 Board Groups: 5 个"
    echo "📋 Boards: 6 个"
    echo "🤖 Agents: 6 个"
    echo ""
    echo "🚀 立即开始使用:"
    echo "   访问: http://localhost:3000"
    echo "   Dashboard: http://localhost:3000/dashboard"
    echo "   Boards: http://localhost:3000/boards"
    echo "   Agents: http://localhost:3000/agents"
    echo ""
    echo "📚 参考文档:"
    echo "   USER_GUIDE.md - 完整使用指南"
    echo "   QUICK_START.md - 快速开始指南"
}

# 运行主流程
main "$@"