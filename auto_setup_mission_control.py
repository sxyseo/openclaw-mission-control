#!/usr/bin/env python3
"""
Mission Control 自动化配置脚本
参照 gstack 理念，一键创建完整的 AI 项目管理环境

功能：
- 自动创建 Board Groups（任务分组）
- 自动配置 Boards（任务板）
- 自动创建 Agents（AI 代理）
- 自动设置 Gateway 连接

使用方法：
    python auto_setup_mission_control.py
"""

import asyncio
import httpx
import json
from typing import Dict, List, Any
from pathlib import Path

# API 配置
API_BASE_URL = "http://localhost:8000"
AUTH_TOKEN = "640d5d3e5e5e5010f8e318489aa88de4bbd111e244a00af17dc0a86eba53b811ab"

# Gateway 配置
GATEWAY_CONFIG = {
    "name": "Main AI Gateway",
    "url": "ws://127.0.0.1:18789",
    "token": "glnb_DPfr0Weu-skGMg7NmKSQ0BviBt9fgjmZjyCgx8",
    "disable_device_pairing": False,
    "workspace_root": "/Users/abel/openclaw-workspace",
    "allow_insecure_tls": False
}

class MissionControlSetup:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    async def create_board_group(self, name: str, description: str) -> Dict[str, Any]:
        """创建 Board Group"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/board-groups",
                headers=self.headers,
                json={
                    "name": name,
                    "description": description
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 创建 Board Group 失败: {name}")
                print(f"   错误: {response.text}")
                return None

    async def create_board(self, name: str, description: str, gateway_id: str, board_group_id: str = None) -> Dict[str, Any]:
        """创建 Board"""
        import re
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

        board_data = {
            "name": name,
            "slug": slug,
            "description": description,
            "gateway_id": gateway_id
        }

        if board_group_id:
            board_data["board_group_id"] = board_group_id

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/boards",
                headers=self.headers,
                json=board_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 创建 Board 失败: {name}")
                print(f"   错误: {response.text}")
                return None

    async def create_agent(self, name: str, board_id: str, description: str) -> Dict[str, Any]:
        """创建 Agent"""
        import re
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/agents",
                headers=self.headers,
                json={
                    "name": name,
                    "slug": slug,
                    "description": description,
                    "board_id": board_id,
                    "status": "online"
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 创建 Agent 失败: {name}")
                print(f"   错误: {response.text}")
                return None

    async def get_or_create_gateway(self) -> Dict[str, Any]:
        """获取或创建 Gateway"""
        async with httpx.AsyncClient() as client:
            # 先尝试获取现有的 gateways
            response = await client.get(
                f"{self.base_url}/api/v1/gateways",
                headers=self.headers
            )

            if response.status_code == 200:
                gateways = response.json()
                if gateways.get("data") and len(gateways["data"]["items"]) > 0:
                    existing_gateway = gateways["data"]["items"][0]
                    print(f"✅ 使用现有 Gateway: {existing_gateway['name']}")
                    return existing_gateway

            # 如果没有现有 gateway，创建新的
            print("🔧 创建新的 Gateway...")
            response = await client.post(
                f"{self.base_url}/api/v1/gateways",
                headers=self.headers,
                json=GATEWAY_CONFIG
            )

            if response.status_code == 200:
                print(f"✅ Gateway 创建成功: {GATEWAY_CONFIG['name']}")
                return response.json()
            else:
                print(f"❌ Gateway 创建失败: {response.text}")
                return None

async def setup_gstack_style_environment():
    """参照 gstack 理念设置完整环境"""
    setup = MissionControlSetup(API_BASE_URL, AUTH_TOKEN)

    print("🚀 开始自动化配置 Mission Control...")
    print("=" * 60)

    # 第一步：创建 Gateway
    print("\n📡 第一步：配置 Gateway")
    print("-" * 40)
    gateway = await setup.get_or_create_gateway()

    if not gateway:
        print("❌ Gateway 配置失败，无法继续")
        return

    gateway_id = gateway["data"]["id"]

    # 第二步：创建 Board Groups（参照 gstack 的项目分类）
    print("\n📊 第二步：创建 Board Groups")
    print("-" * 40)

    board_groups_config = [
        {
            "name": "Personal Projects",
            "description": "管理个人开发项目和学习任务 - 个人项目管理、技能提升、side projects"
        },
        {
            "name": "Work Projects",
            "description": "处理工作相关的开发和维护 - 工作任务、团队协作、商业项目"
        },
        {
            "name": "Learning & Skills",
            "description": "技术学习和能力提升 - 编程语言、框架学习、最佳实践"
        },
        {
            "name": "Tools & Utilities",
            "description": "开发实用工具和脚本 - 自动化工具、效率提升、辅助工具"
        },
        {
            "name": "R&D Experiments",
            "description": "新技术研究和实验项目 - 前沿技术、创新实验、概念验证"
        }
    ]

    created_groups = {}
    for group_config in board_groups_config:
        result = await setup.create_board_group(
            group_config["name"],
            group_config["description"]
        )
        if result:
            created_groups[group_config["name"]] = result["data"]["id"]
            print(f"✅ Board Group 创建成功: {group_config['name']}")

    # 第三步：创建专门的 Boards（参照 gstack 的 15 个专家角色）
    print("\n📋 第三步：创建专家 Boards")
    print("-" * 40)

    boards_config = [
        # 开发专家类
        {
            "name": "Frontend Development",
            "description": "前端开发和UI/UX设计 - React、Vue、Angular等前端技术栈",
            "group": "Personal Projects",
            "agents": ["Frontend Expert", "UI/UX Designer"]
        },
        {
            "name": "Backend Development",
            "description": "后端API和数据库设计 - Python、Node.js、数据库架构",
            "group": "Personal Projects",
            "agents": ["Backend Expert", "Database Architect"]
        },
        {
            "name": "Full Stack Projects",
            "description": "全栈开发项目 - 前后端整合、完整应用开发",
            "group": "Personal Projects",
            "agents": ["Full Stack Developer"]
        },
        # 质量保证类
        {
            "name": "Code Review & Quality",
            "description": "代码审查和质量保证 - 最佳实践、性能优化、安全审查",
            "group": "Tools & Utilities",
            "agents": ["Code Reviewer", "Security Analyst"]
        },
        {
            "name": "QA & Testing",
            "description": "质量保证和测试 - 单元测试、集成测试、自动化测试",
            "group": "Tools & Utilities",
            "agents": ["QA Engineer", "Test Automation Specialist"]
        },
        # 学习类
        {
            "name": "Tech Learning Path",
            "description": "技术学习路径 - 系统学习新技术、编程语言、框架",
            "group": "Learning & Skills",
            "agents": ["Learning Coach", "Mentor Agent"]
        },
        {
            "name": "Documentation Hub",
            "description": "技术文档中心 - API文档、用户手册、README、技术博客",
            "group": "Learning & Skills",
            "agents": ["Technical Writer", "Documentation Specialist"]
        },
        # 管理类
        {
            "name": "Project Management",
            "description": "项目管理中心 - 进度跟踪、资源协调、风险管理",
            "group": "Work Projects",
            "agents": ["Project Manager", "Scrum Master"]
        },
        {
            "name": "Release Management",
            "description": "版本发布管理 - CI/CD、部署流程、版本控制",
            "group": "Work Projects",
            "agents": ["Release Manager", "DevOps Engineer"]
        }
    ]

    created_boards = {}
    for board_config in boards_config:
        group_id = created_groups.get(board_config["group"])
        result = await setup.create_board(
            board_config["name"],
            board_config["description"],
            gateway_id,
            group_id
        )
        if result:
            created_boards[board_config["name"]] = {
                "id": result["data"]["id"],
                "agents": board_config.get("agents", [])
            }
            print(f"✅ Board 创建成功: {board_config['name']}")

    # 第四步：创建专门的 Agents
    print("\n🤖 第四步：创建专家 Agents")
    print("-" * 40)

    agents_config = [
        # 开发专家 (Development)
        {"name": "Frontend Expert", "desc": "前端开发专家 - React、Vue、Angular、UI/UX", "board": "Frontend Development"},
        {"name": "Backend Expert", "desc": "后端开发专家 - API设计、数据库、服务器架构", "board": "Backend Development"},
        {"name": "Full Stack Developer", "desc": "全栈开发工程师 - 前后端整合、完整解决方案", "board": "Full Stack Projects"},

        # 质量保证 (Quality)
        {"name": "Code Reviewer", "desc": "代码审查专家 - 最佳实践、代码质量、性能优化", "board": "Code Review & Quality"},
        {"name": "QA Engineer", "desc": "质量保证工程师 - 测试策略、自动化测试、质量监控", "board": "QA & Testing"},
        {"name": "Security Analyst", "desc": "安全分析师 - 漏洞扫描、安全审查、安全修复", "board": "Code Review & Quality"},

        # 学习和管理 (Learning & Management)
        {"name": "Learning Coach", "desc": "学习教练 - 学习计划制定、进度跟踪、资源推荐", "board": "Tech Learning Path"},
        {"name": "Technical Writer", "desc": "技术文档专家 - API文档、用户手册、技术文章", "board": "Documentation Hub"},
        {"name": "Project Manager", "desc": "项目经理 - 进度管理、资源协调、风险控制", "board": "Project Management"},
        {"name": "Release Manager", "desc": "发布经理 - CI/CD、部署管理、版本控制", "board": "Release Management"}
    ]

    created_agents = {}
    for agent_config in agents_config:
        board_id = created_boards.get(agent_config["board"], {}).get("id")
        if board_id:
            result = await setup.create_agent(
                agent_config["name"],
                board_id,
                agent_config["desc"]
            )
            if result:
                created_agents[agent_config["name"]] = result["data"]["id"]
                print(f"✅ Agent 创建成功: {agent_config['name']} → {agent_config['board']}")

    # 第五步：保存配置信息
    print("\n💾 第五步：保存配置信息")
    print("-" * 40)

    config_summary = {
        "gateway": {
            "id": gateway_id,
            "name": GATEWAY_CONFIG["name"],
            "url": GATEWAY_CONFIG["url"]
        },
        "board_groups": created_groups,
        "boards": {name: {"id": info["id"], "group": boards_config[[b["name"] for b in boards_config if b["name"] == name][0]]["group"]} for name, info in created_boards.items()},
        "agents": {name: {"id": agent_id, "board": agent_config["board"]} for name, agent_id in created_agents.items()}
    }

    config_file = Path("mission_control_config.json")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_summary, f, indent=2, ensure_ascii=False)

    print(f"✅ 配置信息已保存到: {config_file.absolute()}")

    # 总结
    print("\n" + "=" * 60)
    print("🎉 自动化配置完成！")
    print("=" * 60)
    print(f"📊 Board Groups: {len(created_groups)} 个")
    print(f"📋 Boards: {len(created_boards)} 个")
    print(f"🤖 Agents: {len(created_agents)} 个")
    print(f"🌐 Gateway: 1 个")

    print("\n🚀 立即开始使用:")
    print(f"   访问: {API_BASE_URL.replace('8000', '3000')}")
    print(f"   Dashboard: {API_BASE_URL.replace('8000', '3000')}/dashboard")
    print(f"   Boards: {API_BASE_URL.replace('8000', '3000')}/boards")
    print(f"   Agents: {API_BASE_URL.replace('8000', '3000')}/agents")

    print("\n📚 参考文档:")
    print("   USER_GUIDE.md - 完整使用指南")
    print("   QUICK_START.md - 快速开始指南")

    return config_summary

if __name__ == "__main__":
    try:
        asyncio.run(setup_gstack_style_environment())
    except Exception as e:
        print(f"❌ 自动化配置失败: {str(e)}")
        import traceback
        traceback.print_exc()