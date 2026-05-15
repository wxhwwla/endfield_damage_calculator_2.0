#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选择面板组件模块

此模块包含选择面板中可复用的子组件类：
- SkillLevelPanel: 技能等级选择面板（角色专用）
- SpecialAbilityPanel: 特殊能力选择面板（武器专用）
- TrustPanel: 信赖等级选择面板（角色专用）

这些组件被设计为独立的、可组合的 UI 模块，便于维护和测试。
"""

import customtkinter as ctk
from typing import List, Dict, Any, Optional


class TrustPanel:
    """
    信赖等级选择面板
    
    提供角色信赖等级的滑块选择功能（0-4级）。
    
    属性：
        trust_level: 当前选中的信赖等级（StringVar）
    """
    
    def __init__(self, parent_frame: ctk.CTkFrame, my_font: ctk.CTkFont):
        """
        初始化信赖面板
        
        参数：
            parent_frame: 父框架容器
            my_font: 使用的字体配置
        """
        self.parent_frame = parent_frame
        self.my_font = my_font
        
        # 信赖等级变量
        self.trust_level: ctk.StringVar = ctk.StringVar(value="0")
        
        # UI控件
        self.trust_label: ctk.CTkLabel | None = None
        self.trust_slider: ctk.CTkSlider | None = None
        self.trust_name_label: ctk.CTkLabel | None = None
        
        # 构建GUI
        self._build_gui()
    
    def _build_gui(self) -> None:
        """构建信赖滑块GUI"""
        # 信赖标签（上方）
        self.trust_name_label = ctk.CTkLabel(self.parent_frame, text="信赖", font=self.my_font)
        self.trust_name_label.pack(anchor="w")
        
        # 信赖滑块框架（下方）
        trust_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        trust_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        # 等级显示标签（右侧，固定宽度30）
        self.trust_label = ctk.CTkLabel(trust_frame, text="0", font=self.my_font, width=30)
        self.trust_label.pack(side="right")
        
        # 滑块（左侧，填充剩余空间）
        self.trust_slider = ctk.CTkSlider(
            trust_frame,
            from_=0,
            to=4,
            number_of_steps=4,
            command=self._on_slider_change
        )
        self.trust_slider.pack(side="left", fill="x", expand=True)
        self.trust_slider.set(0)
    
    def _on_slider_change(self, value: float) -> None:
        """
        滑块值变化事件处理
        
        参数：
            value: 滑块当前值（float类型）
        """
        level = int(value)
        if self.trust_label:
            self.trust_label.configure(text=str(level))
        self.trust_level.set(str(level))


class SpecialAbilityPanel:
    """
    特殊能力选择面板
    
    提供武器特殊能力等级的滑块选择功能（最多3个特殊能力）。
    第三个特殊能力需要开关启用。
    
    属性：
        special_ability_1_level: 特殊能力1等级（StringVar）
        special_ability_2_level: 特殊能力2等级（StringVar）
        special_ability_3_level: 特殊能力3等级（StringVar）
        current_special_ability_1_name: 当前特殊能力1名称
        current_special_ability_2_name: 当前特殊能力2名称
        current_special_ability_3_name: 当前特殊能力3名称
    """
    
    def __init__(self, parent_frame: ctk.CTkFrame, my_font: ctk.CTkFont):
        """
        初始化特殊能力面板
        
        参数：
            parent_frame: 父框架容器
            my_font: 使用的字体配置
        """
        self.parent_frame = parent_frame
        self.my_font = my_font
        
        # 特殊能力等级变量
        self.special_ability_1_level: ctk.StringVar = ctk.StringVar(value="1")
        self.special_ability_2_level: ctk.StringVar = ctk.StringVar(value="1")
        self.special_ability_3_level: ctk.StringVar = ctk.StringVar(value="0")
        
        # 当前特殊能力名称
        self.current_special_ability_1_name: str = ""
        self.current_special_ability_2_name: str = ""
        self.current_special_ability_3_name: str = ""
        
        # 第三个特殊能力开关状态
        self.special_ability_3_enabled = ctk.BooleanVar(value=False)
        
        # UI控件
        self._ability_1_name_label: ctk.CTkLabel | None = None
        self._ability_1_label: ctk.CTkLabel | None = None
        self._ability_1_slider: ctk.CTkSlider | None = None
        
        self._ability_2_name_label: ctk.CTkLabel | None = None
        self._ability_2_label: ctk.CTkLabel | None = None
        self._ability_2_slider: ctk.CTkSlider | None = None
        
        self._ability_3_name_label: ctk.CTkLabel | None = None
        self._ability_3_label: ctk.CTkLabel | None = None
        self._ability_3_slider: ctk.CTkSlider | None = None
        self._ability_3_switch: ctk.CTkSwitch | None = None
        
        # 滑块框架引用（用于隐藏/显示）
        self._ability_1_frame: ctk.CTkFrame | None = None
        self._ability_2_frame: ctk.CTkFrame | None = None
        self._ability_3_header_frame: ctk.CTkFrame | None = None
        self._ability_3_frame: ctk.CTkFrame | None = None
        
        # 构建GUI
        self._build_gui()
    
    def _build_gui(self) -> None:
        """构建特殊能力滑块GUI"""
        # 特殊能力1
        self._ability_1_name_label = ctk.CTkLabel(self.parent_frame, text="特殊能力1", font=self.my_font)
        self._ability_1_name_label.pack(anchor="w")
        
        self._ability_1_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self._ability_1_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self._ability_1_label = ctk.CTkLabel(self._ability_1_frame, text="1", font=self.my_font, width=30)
        self._ability_1_label.pack(side="right")
        
        self._ability_1_slider = ctk.CTkSlider(
            self._ability_1_frame,
            from_=1,
            to=9,
            number_of_steps=8,
            command=self._on_ability_1_change
        )
        self._ability_1_slider.pack(side="left", fill="x", expand=True)
        self._ability_1_slider.set(1)
        
        # 特殊能力2
        self._ability_2_name_label = ctk.CTkLabel(self.parent_frame, text="特殊能力2", font=self.my_font)
        self._ability_2_name_label.pack(anchor="w")
        
        self._ability_2_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self._ability_2_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self._ability_2_label = ctk.CTkLabel(self._ability_2_frame, text="1", font=self.my_font, width=30)
        self._ability_2_label.pack(side="right")
        
        self._ability_2_slider = ctk.CTkSlider(
            self._ability_2_frame,
            from_=1,
            to=9,
            number_of_steps=8,
            command=self._on_ability_2_change
        )
        self._ability_2_slider.pack(side="left", fill="x", expand=True)
        self._ability_2_slider.set(1)
        
        # 特殊能力3（默认隐藏）
        self._ability_3_header_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        
        self._ability_3_name_label = ctk.CTkLabel(self._ability_3_header_frame, text="特殊能力3", font=self.my_font)
        self._ability_3_name_label.pack(side="left")
        
        self._ability_3_switch = ctk.CTkSwitch(
            self._ability_3_header_frame,
            text="",
            variable=self.special_ability_3_enabled,
            command=self._on_ability_3_switch_change,
            width=40
        )
        self._ability_3_switch.pack(side="right")
        
        self._ability_3_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        
        self._ability_3_label = ctk.CTkLabel(self._ability_3_frame, text="0", font=self.my_font, width=30)
        self._ability_3_label.pack(side="right")
        
        self._ability_3_slider = ctk.CTkSlider(
            self._ability_3_frame,
            from_=1,
            to=9,
            number_of_steps=8,
            command=self._on_ability_3_change,
            state="disabled"
        )
        self._ability_3_slider.pack(side="left", fill="x", expand=True)
        self._ability_3_slider.set(1)
    
    def _on_ability_1_change(self, value: float) -> None:
        """特殊能力1滑块值变化事件处理"""
        level = int(value)
        if self._ability_1_label:
            self._ability_1_label.configure(text=str(level))
        self.special_ability_1_level.set(str(level))
    
    def _on_ability_2_change(self, value: float) -> None:
        """特殊能力2滑块值变化事件处理"""
        level = int(value)
        if self._ability_2_label:
            self._ability_2_label.configure(text=str(level))
        self.special_ability_2_level.set(str(level))
    
    def _on_ability_3_change(self, value: float) -> None:
        """特殊能力3滑块值变化事件处理"""
        level = int(value)
        if self._ability_3_label:
            self._ability_3_label.configure(text=str(level))
        self.special_ability_3_level.set(str(level))
    
    def _on_ability_3_switch_change(self) -> None:
        """特殊能力3开关状态变化事件处理"""
        enabled = self.special_ability_3_enabled.get()
        
        if self._ability_3_slider:
            self._ability_3_slider.configure(state="normal" if enabled else "disabled")
        
        if enabled:
            if self._ability_3_slider:
                current_value = int(self._ability_3_slider.get())
                self.special_ability_3_level.set(str(current_value))
                if self._ability_3_label:
                    self._ability_3_label.configure(text=str(current_value))
        else:
            self.special_ability_3_level.set("0")
            if self._ability_3_label:
                self._ability_3_label.configure(text="0")
    
    def refresh(self, weapon_data: Dict[str, Any]) -> None:
        """
        根据武器数据刷新特殊能力面板
        
        参数：
            weapon_data: 武器数据字典
        """
        special_abilities = self._extract_special_abilities(weapon_data)
        
        if len(special_abilities) >= 2:
            self.current_special_ability_1_name = special_abilities[0]
            self.current_special_ability_2_name = special_abilities[1]
            
            # 更新标签显示
            if self._ability_1_name_label:
                self._ability_1_name_label.configure(text=self.current_special_ability_1_name)
            if self._ability_1_label:
                self._ability_1_label.configure(text="1")
            if self._ability_2_name_label:
                self._ability_2_name_label.configure(text=self.current_special_ability_2_name)
            if self._ability_2_label:
                self._ability_2_label.configure(text="1")
            
            # 重置等级
            self.special_ability_1_level.set("1")
            self.special_ability_2_level.set("1")
            if self._ability_1_slider:
                self._ability_1_slider.set(1)
            if self._ability_2_slider:
                self._ability_2_slider.set(1)
            
            # 显示前两个滑块
            self._show_abilities(1, 2)
            
            # 处理第三个特殊能力
            if len(special_abilities) >= 3:
                self.current_special_ability_3_name = special_abilities[2]
                if self._ability_3_name_label:
                    self._ability_3_name_label.configure(text=self.current_special_ability_3_name)
                # 默认关闭状态，显示0级
                if self._ability_3_label:
                    self._ability_3_label.configure(text="0")
                if self._ability_3_slider:
                    self._ability_3_slider.configure(state="disabled")
                    self._ability_3_slider.set(1)  # 复位滑块值到1
                self.special_ability_3_enabled.set(False)
                self.special_ability_3_level.set("0")
                self._show_ability_3()
            else:
                self.current_special_ability_3_name = ""
                self._hide_ability_3()
        else:
            self.current_special_ability_1_name = ""
            self.current_special_ability_2_name = ""
            self.current_special_ability_3_name = ""
            self._hide_all_abilities()
    
    def _extract_special_abilities(self, weapon_data: Dict[str, Any]) -> List[str]:
        """
        从武器数据中提取特殊能力字段名
        
        参数：
            weapon_data: 武器数据字典
        
        返回：
            特殊能力字段名列表
        """
        excluded_fields = {'名称', '类型', '星级', '等级', '潜能', '基础攻击力', '特殊能力'}
        keys = list(weapon_data.keys())
        
        try:
            base_attack_index = keys.index('基础攻击力')
        except ValueError:
            return []
        
        try:
            special_ability_index = keys.index('特殊能力')
        except ValueError:
            return []
        
        special_abilities = []
        for key in keys[base_attack_index + 1:special_ability_index]:
            if key not in excluded_fields and isinstance(weapon_data[key], list):
                special_abilities.append(key)
        
        # 检查特殊能力字段内部是否有第三个特殊能力
        special_ability_field = weapon_data.get('特殊能力', [])
        if isinstance(special_ability_field, list) and len(special_ability_field) >= 3:
            if isinstance(special_ability_field[1], str) and special_ability_field[1]:
                special_abilities.append(special_ability_field[1])
        
        return special_abilities
    
    def _show_abilities(self, *indices: int) -> None:
        """显示指定的特殊能力滑块"""
        for idx in indices:
            if idx == 1:
                if self._ability_1_name_label:
                    self._ability_1_name_label.pack(anchor="w")
                if self._ability_1_frame:
                    self._ability_1_frame.pack(fill="x", padx=10, pady=(0, 5))
            elif idx == 2:
                if self._ability_2_name_label:
                    self._ability_2_name_label.pack(anchor="w")
                if self._ability_2_frame:
                    self._ability_2_frame.pack(fill="x", padx=10, pady=(0, 5))
    
    def _hide_all_abilities(self) -> None:
        """隐藏所有特殊能力滑块"""
        if self._ability_1_name_label:
            self._ability_1_name_label.pack_forget()
        if self._ability_1_frame:
            self._ability_1_frame.pack_forget()
        if self._ability_2_name_label:
            self._ability_2_name_label.pack_forget()
        if self._ability_2_frame:
            self._ability_2_frame.pack_forget()
        self._hide_ability_3()
    
    def _show_ability_3(self) -> None:
        """显示第三个特殊能力滑块"""
        if self._ability_3_header_frame:
            self._ability_3_header_frame.pack(fill="x", pady=(5, 0))
        if self._ability_3_frame:
            self._ability_3_frame.pack(fill="x", padx=10, pady=(0, 5))
    
    def _hide_ability_3(self) -> None:
        """隐藏第三个特殊能力滑块"""
        if self._ability_3_header_frame:
            self._ability_3_header_frame.pack_forget()
        if self._ability_3_frame:
            self._ability_3_frame.pack_forget()
    
    def hide(self) -> None:
        """隐藏所有特殊能力面板"""
        self._hide_all_abilities()
    
    def show(self) -> None:
        """显示所有特殊能力面板（根据当前数据）"""
        # 如果有特殊能力数据，显示前两个
        if self.current_special_ability_1_name:
            self._show_abilities(1, 2)
        if self.current_special_ability_3_name:
            self._show_ability_3()


class SkillLevelPanel:
    """
    技能等级选择面板
    
    提供角色技能等级的滑块选择功能（战技、连携技、终结技）。
    
    属性：
        skill_1_level: 战技等级（StringVar）
        skill_2_level: 连携技等级（StringVar）
        skill_3_level: 终结技等级（StringVar）
    """
    
    def __init__(self, parent_frame: ctk.CTkFrame, my_font: ctk.CTkFont, on_change_callback=None):
        """
        初始化技能等级面板
        
        参数：
            parent_frame: 父框架容器
            my_font: 使用的字体配置
            on_change_callback: 技能等级变化时的回调函数
        """
        self.parent_frame = parent_frame
        self.my_font = my_font
        self.on_change_callback = on_change_callback
        
        # 技能等级变量
        self.skill_1_level: ctk.StringVar = ctk.StringVar(value="1")
        self.skill_2_level: ctk.StringVar = ctk.StringVar(value="1")
        self.skill_3_level: ctk.StringVar = ctk.StringVar(value="1")
        
        # 当前技能名称
        self.current_skill_1_name: str = "战技"
        self.current_skill_2_name: str = "连携技"
        self.current_skill_3_name: str = "终结技"
        
        # 技能倍率数据引用
        self._skill_1_data: list = []
        self._skill_2_data: list = []
        self._skill_3_data: list = []
        
        # UI控件
        self._skill_1_name_label: ctk.CTkLabel | None = None
        self._skill_1_label: ctk.CTkLabel | None = None
        self._skill_1_slider: ctk.CTkSlider | None = None
        self._skill_1_frame: ctk.CTkFrame | None = None
        
        self._skill_2_name_label: ctk.CTkLabel | None = None
        self._skill_2_label: ctk.CTkLabel | None = None
        self._skill_2_slider: ctk.CTkSlider | None = None
        self._skill_2_frame: ctk.CTkFrame | None = None
        
        self._skill_3_name_label: ctk.CTkLabel | None = None
        self._skill_3_label: ctk.CTkLabel | None = None
        self._skill_3_slider: ctk.CTkSlider | None = None
        self._skill_3_frame: ctk.CTkFrame | None = None
        
        # 构建GUI
        self._build_gui()
    
    def _build_gui(self) -> None:
        """构建技能等级滑块GUI"""
        # 战技等级
        self._skill_1_name_label = ctk.CTkLabel(self.parent_frame, text="战技", font=self.my_font)
        self._skill_1_name_label.pack(anchor="w")
        
        self._skill_1_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self._skill_1_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self._skill_1_label = ctk.CTkLabel(self._skill_1_frame, text="1", font=self.my_font, width=30)
        self._skill_1_label.pack(side="right")
        
        self._skill_1_slider = ctk.CTkSlider(
            self._skill_1_frame,
            from_=1,
            to=12,
            number_of_steps=11,
            command=self._on_skill_1_change
        )
        self._skill_1_slider.pack(side="left", fill="x", expand=True)
        self._skill_1_slider.set(1)
        
        # 连携技等级
        self._skill_2_name_label = ctk.CTkLabel(self.parent_frame, text="连携技", font=self.my_font)
        self._skill_2_name_label.pack(anchor="w")
        
        self._skill_2_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self._skill_2_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self._skill_2_label = ctk.CTkLabel(self._skill_2_frame, text="1", font=self.my_font, width=30)
        self._skill_2_label.pack(side="right")
        
        self._skill_2_slider = ctk.CTkSlider(
            self._skill_2_frame,
            from_=1,
            to=12,
            number_of_steps=11,
            command=self._on_skill_2_change
        )
        self._skill_2_slider.pack(side="left", fill="x", expand=True)
        self._skill_2_slider.set(1)
        
        # 终结技等级
        self._skill_3_name_label = ctk.CTkLabel(self.parent_frame, text="终结技", font=self.my_font)
        self._skill_3_name_label.pack(anchor="w")
        
        self._skill_3_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self._skill_3_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self._skill_3_label = ctk.CTkLabel(self._skill_3_frame, text="1", font=self.my_font, width=30)
        self._skill_3_label.pack(side="right")
        
        self._skill_3_slider = ctk.CTkSlider(
            self._skill_3_frame,
            from_=1,
            to=12,
            number_of_steps=11,
            command=self._on_skill_3_change
        )
        self._skill_3_slider.pack(side="left", fill="x", expand=True)
        self._skill_3_slider.set(1)
    
    def _on_skill_1_change(self, value: float) -> None:
        """战技滑块值变化事件处理"""
        level = int(value)
        if self._skill_1_label:
            self._skill_1_label.configure(text=str(level))
        self.skill_1_level.set(str(level))
        if self.on_change_callback:
            self.on_change_callback()
    
    def _on_skill_2_change(self, value: float) -> None:
        """连携技滑块值变化事件处理"""
        level = int(value)
        if self._skill_2_label:
            self._skill_2_label.configure(text=str(level))
        self.skill_2_level.set(str(level))
        if self.on_change_callback:
            self.on_change_callback()
    
    def _on_skill_3_change(self, value: float) -> None:
        """终结技滑块值变化事件处理"""
        level = int(value)
        if self._skill_3_label:
            self._skill_3_label.configure(text=str(level))
        self.skill_3_level.set(str(level))
        if self.on_change_callback:
            self.on_change_callback()
    
    def refresh(self, char_data: Dict[str, Any]) -> None:
        """
        根据角色数据刷新技能等级面板
        
        参数：
            char_data: 角色数据字典
        """
        # 获取技能倍率数据
        self._skill_1_data = char_data.get("战技倍率", [])
        self._skill_2_data = char_data.get("连携技倍率", [])
        self._skill_3_data = char_data.get("终结技倍率", [])
        
        # 检查是否有多个技能
        # 战技
        if len(self._skill_1_data) >= 1:
            self.current_skill_1_name = "战技"
            if self._skill_1_name_label:
                self._skill_1_name_label.configure(text=self.current_skill_1_name)
            if self._skill_1_label:
                self._skill_1_label.configure(text="1")
            self.skill_1_level.set("1")
            if self._skill_1_slider:
                self._skill_1_slider.set(1)
            self._show_skill_1()
        else:
            self.current_skill_1_name = ""
            self._hide_skill_1()
        
        # 连携技
        if len(self._skill_2_data) >= 1:
            self.current_skill_2_name = "连携技"
            if self._skill_2_name_label:
                self._skill_2_name_label.configure(text=self.current_skill_2_name)
            if self._skill_2_label:
                self._skill_2_label.configure(text="1")
            self.skill_2_level.set("1")
            if self._skill_2_slider:
                self._skill_2_slider.set(1)
            self._show_skill_2()
        else:
            self.current_skill_2_name = ""
            self._hide_skill_2()
        
        # 终结技
        if len(self._skill_3_data) >= 1:
            self.current_skill_3_name = "终结技"
            if self._skill_3_name_label:
                self._skill_3_name_label.configure(text=self.current_skill_3_name)
            if self._skill_3_label:
                self._skill_3_label.configure(text="1")
            self.skill_3_level.set("1")
            if self._skill_3_slider:
                self._skill_3_slider.set(1)
            self._show_skill_3()
        else:
            self.current_skill_3_name = ""
            self._hide_skill_3()
    
    def _show_skill_1(self) -> None:
        """显示战技滑块"""
        if self._skill_1_name_label:
            self._skill_1_name_label.pack(anchor="w")
        if self._skill_1_frame:
            self._skill_1_frame.pack(fill="x", padx=10, pady=(0, 5))
    
    def _hide_skill_1(self) -> None:
        """隐藏战技滑块"""
        if self._skill_1_name_label:
            self._skill_1_name_label.pack_forget()
        if self._skill_1_frame:
            self._skill_1_frame.pack_forget()
    
    def _show_skill_2(self) -> None:
        """显示连携技滑块"""
        if self._skill_2_name_label:
            self._skill_2_name_label.pack(anchor="w")
        if self._skill_2_frame:
            self._skill_2_frame.pack(fill="x", padx=10, pady=(0, 5))
    
    def _hide_skill_2(self) -> None:
        """隐藏连携技滑块"""
        if self._skill_2_name_label:
            self._skill_2_name_label.pack_forget()
        if self._skill_2_frame:
            self._skill_2_frame.pack_forget()
    
    def _show_skill_3(self) -> None:
        """显示终结技滑块"""
        if self._skill_3_name_label:
            self._skill_3_name_label.pack(anchor="w")
        if self._skill_3_frame:
            self._skill_3_frame.pack(fill="x", padx=10, pady=(0, 5))
    
    def _hide_skill_3(self) -> None:
        """隐藏终结技滑块"""
        if self._skill_3_name_label:
            self._skill_3_name_label.pack_forget()
        if self._skill_3_frame:
            self._skill_3_frame.pack_forget()
    
    def hide(self) -> None:
        """隐藏所有技能等级面板"""
        self._hide_skill_1()
        self._hide_skill_2()
        self._hide_skill_3()
    
    def show(self) -> None:
        """显示所有技能等级面板（根据当前数据）"""
        if self.current_skill_1_name:
            self._show_skill_1()
        if self.current_skill_2_name:
            self._show_skill_2()
        if self.current_skill_3_name:
            self._show_skill_3()

