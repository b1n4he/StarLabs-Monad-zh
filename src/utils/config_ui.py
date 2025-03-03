import customtkinter as ctk
import yaml
import os


class ConfigUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Define color scheme
        self.colors = {
            "bg": "#121212",  # Slightly lighter black background
            "frame_bg": "#1e1e1e",  # Slightly lighter frame background
            "accent": "#B8860B",  # More muted gold/yellow (DarkGoldenrod)
            "text": "#ffffff",  # White text
            "entry_bg": "#1e1e1e",  # Dark input background
            "hover": "#8B6914",  # Darker muted yellow for hover
        }

        # Standardize input widths
        self.input_sizes = {
            "tiny": 70,  # For small numbers (1-2 digits)
            "small": 115,  # For short text/numbers
            "medium": 180,  # For medium length text
            "large": 250,  # For long text
            "extra_large": 350,  # For very long text/lists
        }

        self.root = ctk.CTk()
        self.root.title("StarLabs Monad 配置")
        self.root.geometry("1250x800")
        self.root.minsize(1250, 800)  # Set minimum window size
        self.root.configure(fg_color=self.colors["bg"])

        # Create header frame
        header_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg"])
        header_frame.pack(
            fill="x", padx=50, pady=(20, 0)
        )  # Increased left/right padding

        # Header on the left
        header = ctk.CTkLabel(
            header_frame,
            text="🌟 StarLabs Monad 配置",
            font=("Helvetica", 24, "bold"),
            text_color=self.colors["accent"],
            anchor="w",
        )
        header.pack(side="left", padx=5)  # Added left padding

        # Save button in the top right
        self.save_button = ctk.CTkButton(
            header_frame,
            text="⚡ 保存",  # Changed icon and made text uppercase
            command=self._save_and_close,
            font=("Helvetica", 18, "bold"),  # Increased font size
            height=45,
            width=160,  # Slightly wider
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            text_color=self.colors["text"],
            corner_radius=10,
        )
        self.save_button.pack(side="right", padx=5)  # Added right padding

        # Create main frame with scrollbar
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg"])
        self.main_frame.pack(fill="both", expand=True, padx=5)

        # Add canvas and scrollbar
        self.canvas = ctk.CTkCanvas(
            self.main_frame, bg=self.colors["bg"], highlightthickness=0
        )
        self.scrollbar = ctk.CTkScrollbar(
            self.main_frame,
            orientation="vertical",
            command=self.canvas.yview,
            fg_color=self.colors["frame_bg"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["hover"],
        )
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=self.colors["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Pack scrollbar components
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create window in canvas with proper width
        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_width(),  # Use canvas width
        )

        # Update canvas width when window is resized
        def update_canvas_width(event):
            self.canvas.itemconfig(
                self.canvas.find_withtag("all")[0], width=event.width
            )

        self.canvas.bind("<Configure>", update_canvas_width)

        # Configure scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.load_config()
        self.create_widgets()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.yaml")
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def create_range_inputs(self, parent, label, config_value, width=120):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame_bg"])
        frame.pack(fill="x", pady=5)
        frame.grid_columnconfigure(1, weight=1)  # Column for inputs will expand

        ctk.CTkLabel(
            frame,
            text=f"{label}:",
            width=200,
            anchor="w",
            font=("Helvetica", 12, "bold"),
            text_color=self.colors["text"],
        ).grid(row=0, column=0, padx=(10, 10), sticky="w")

        input_frame = ctk.CTkFrame(frame, fg_color=self.colors["frame_bg"])
        input_frame.grid(row=0, column=1, sticky="e", padx=(0, 10))

        min_entry = ctk.CTkEntry(
            input_frame,
            width=width,
            font=("Helvetica", 12, "bold"),
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["accent"],
        )
        min_entry.pack(side="left", padx=(0, 5))
        min_entry.insert(0, str(config_value[0]))

        ctk.CTkLabel(
            input_frame,
            text=" - ",
            font=("Helvetica", 12, "bold"),
            text_color=self.colors["text"],
        ).pack(side="left", padx=5)

        max_entry = ctk.CTkEntry(
            input_frame,
            width=width,
            font=("Helvetica", 12, "bold"),
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["accent"],
        )
        max_entry.pack(side="left", padx=(5, 0))
        max_entry.insert(0, str(config_value[1]))

        return min_entry, max_entry

    def create_single_input(self, parent, label, config_value, width=300):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame_bg"])
        frame.pack(fill="x", pady=5)
        frame.grid_columnconfigure(1, weight=1)  # Column for input will expand

        ctk.CTkLabel(
            frame,
            text=f"{label}:",
            width=200,
            anchor="w",
            font=("Helvetica", 12, "bold"),
            text_color=self.colors["text"],
        ).grid(row=0, column=0, padx=(10, 10), sticky="w")

        entry = ctk.CTkEntry(
            frame,
            width=width,
            font=("Helvetica", 12, "bold"),
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["accent"],
        )
        entry.grid(row=0, column=1, padx=(0, 10), sticky="e")
        entry.insert(0, str(config_value))

        return entry

    def create_checkbox(self, parent, label, config_value):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame_bg"])
        frame.pack(fill="x", pady=5)
        frame.grid_columnconfigure(0, weight=1)

        var = ctk.BooleanVar(value=config_value)
        checkbox = ctk.CTkCheckBox(
            frame,
            text=label,
            variable=var,
            font=("Helvetica", 12, "bold"),
            text_color=self.colors["text"],
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            border_color=self.colors["accent"],
        )
        checkbox.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        return var

    def create_section(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame_bg"])
        frame.pack(fill="x", padx=5, pady=5)

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Helvetica", 14, "bold"),
            text_color=self.colors["accent"],
        )
        label.pack(anchor="w", padx=10, pady=10)

        return frame

    def create_category_header(self, parent, title):
        header = ctk.CTkLabel(
            parent,
            text=title,
            font=("Helvetica", 18, "bold"),
            text_color=self.colors["accent"],
        )
        header.pack(fill="x", pady=(20, 10), padx=5)

    def create_network_checkboxes(self, parent, label, config_value):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame_bg"])
        frame.pack(fill="x", pady=5)

        label = ctk.CTkLabel(
            frame,
            text=f"{label}:",
            width=200,
            anchor="w",
            font=("Helvetica", 12, "bold"),
            text_color=self.colors["text"],
        )
        label.pack(anchor="w", padx=10, pady=(5, 0))

        networks_frame = ctk.CTkFrame(frame, fg_color=self.colors["frame_bg"])
        networks_frame.pack(fill="x", padx=10, pady=5)

        networks = ["Arbitrum", "Base", "Optimism"]
        checkboxes = []

        for network in networks:
            var = ctk.BooleanVar(value=network in config_value)
            checkbox = ctk.CTkCheckBox(
                networks_frame,
                text=network,
                variable=var,
                font=("Helvetica", 12, "bold"),
                text_color=self.colors["text"],
                fg_color=self.colors["accent"],
                hover_color=self.colors["hover"],
                border_color=self.colors["accent"],
            )
            checkbox.pack(side="left", padx=10, pady=5)
            checkboxes.append((network, var))

        return checkboxes

    def create_nft_contracts_list(self, parent, label, config_value):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame_bg"])
        frame.pack(fill="x", pady=5)

        label = ctk.CTkLabel(
            frame,
            text=f"{label}:",
            width=200,
            anchor="w",
            font=("Helvetica", 12, "bold"),
            text_color=self.colors["text"],
        )
        label.pack(anchor="w", padx=10, pady=(5, 0))

        # Создаем фрейм для списка контрактов
        contracts_frame = ctk.CTkFrame(frame, fg_color=self.colors["frame_bg"])
        contracts_frame.pack(fill="x", padx=10, pady=5)

        # Создаем Listbox для отображения контрактов
        contracts_list = ctk.CTkTextbox(
            contracts_frame,
            height=100,
            width=self.input_sizes["extra_large"],
            font=("Helvetica", 12),
            text_color=self.colors["text"],
            fg_color=self.colors["entry_bg"],
            border_color=self.colors["accent"],
        )
        contracts_list.pack(side="left", padx=(0, 10), fill="both", expand=True)

        # Добавляем существующие контракты
        contracts_list.insert("1.0", "\n".join(config_value))

        # Создаем фрейм для кнопок управления
        buttons_frame = ctk.CTkFrame(contracts_frame, fg_color=self.colors["frame_bg"])
        buttons_frame.pack(side="left", fill="y")

        # Поле для ввода нового контракта
        new_contract_entry = ctk.CTkEntry(
            buttons_frame,
            width=200,
            font=("Helvetica", 12),
            placeholder_text="输入新的合约地址",
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["text"],
            border_color=self.colors["accent"],
        )
        new_contract_entry.pack(pady=(0, 5))

        def add_contract():
            new_contract = new_contract_entry.get().strip()
            if new_contract:
                current_text = contracts_list.get("1.0", "end-1c")
                if current_text:
                    contracts_list.insert("end", f"\n{new_contract}")
                else:
                    contracts_list.insert("1.0", new_contract)
                new_contract_entry.delete(0, "end")

        def remove_selected():
            try:
                selection = contracts_list.tag_ranges("sel")
                if selection:
                    contracts_list.delete(selection[0], selection[1])
            except:
                pass

        # Кнопки управления
        add_button = ctk.CTkButton(
            buttons_frame,
            text="增加合约",
            command=add_contract,
            font=("Helvetica", 12, "bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            text_color=self.colors["text"],
            width=120,
        )
        add_button.pack(pady=5)

        remove_button = ctk.CTkButton(
            buttons_frame,
            text="移除选择",
            command=remove_selected,
            font=("Helvetica", 12, "bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["hover"],
            text_color=self.colors["text"],
            width=120,
        )
        remove_button.pack(pady=5)

        return contracts_list

    def create_widgets(self):
        """
        创建界面上的所有控件，将其分为左右两列布局
        """
        # 创建一个框架用于包含左右两列，填充整个可用空间
        columns_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.colors["bg"])
        columns_frame.pack(fill="both", expand=True)

        # 创建左列框架
        left_column = ctk.CTkFrame(columns_frame, fg_color=self.colors["bg"])
        left_column.pack(side="left", fill="both", expand=True, padx=5)

        # 创建右列框架
        right_column = ctk.CTkFrame(columns_frame, fg_color=self.colors["bg"])
        right_column.pack(side="left", fill="both", expand=True, padx=5)

        # 左列内容

        # 通用设置分类
        self.create_category_header(left_column, "⚙️ 通用设置")
        # 创建一个设置部分
        settings = self.create_section(left_column, "设置")
        # 创建线程数输入框
        self.threads_entry = self.create_single_input(
            settings,
            "线程数",
            self.config["SETTINGS"]["THREADS"],
            width=self.input_sizes["tiny"],
        )
        # 创建尝试次数输入框
        self.attempts_entry = self.create_single_input(
            settings,
            "尝试次数",
            self.config["SETTINGS"]["ATTEMPTS"],
            width=self.input_sizes["tiny"],
        )
        # 创建账户范围输入框
        self.acc_range_start, self.acc_range_end = self.create_range_inputs(
            settings,
            "账户范围",
            self.config["SETTINGS"]["ACCOUNTS_RANGE"],
            width=self.input_sizes["tiny"],
        )

        # 添加精确使用的账户输入框
        self.exact_accounts = self.create_single_input(
            settings,
            "精确使用的账户",
            ", ".join(map(str, self.config["SETTINGS"]["EXACT_ACCOUNTS_TO_USE"])),
            width=self.input_sizes["large"],
        )

        # 创建尝试间暂停时间范围输入框
        self.pause_attempts_min, self.pause_attempts_max = self.create_range_inputs(
            settings,
            "尝试间暂停时间",
            self.config["SETTINGS"]["PAUSE_BETWEEN_ATTEMPTS"],
            width=self.input_sizes["small"],
        )
        # 创建交换间暂停时间范围输入框
        self.pause_swaps_min, self.pause_swaps_max = self.create_range_inputs(
            settings,
            "交换间暂停时间",
            self.config["SETTINGS"]["PAUSE_BETWEEN_SWAPS"],
            width=self.input_sizes["small"],
        )
        # 创建账户间随机暂停时间范围输入框
        self.pause_accounts_min, self.pause_accounts_max = self.create_range_inputs(
            settings,
            "账户间随机暂停时间",
            self.config["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACCOUNTS"],
            width=self.input_sizes["small"],
        )
        # 创建操作间随机暂停时间范围输入框
        self.pause_actions_min, self.pause_actions_max = self.create_range_inputs(
            settings,
            "操作间随机暂停时间",
            self.config["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACTIONS"],
            width=self.input_sizes["small"],
        )
        # 创建初始化随机暂停时间范围输入框
        self.init_pause_min, self.init_pause_max = self.create_range_inputs(
            settings,
            "初始化随机暂停时间",
            self.config["SETTINGS"]["RANDOM_INITIALIZATION_PAUSE"],
            width=self.input_sizes["small"],
        )
        # 创建浏览器暂停乘数输入框
        self.browser_multiplier = self.create_single_input(
            settings,
            "浏览器暂停乘数",
            self.config["SETTINGS"]["BROWSER_PAUSE_MULTIPLIER"],
            width=self.input_sizes["tiny"],
        )

        # 添加Telegram设置
        self.telegram_ids = self.create_single_input(
            settings,
            "Telegram用户ID",
            ", ".join(map(str, self.config["SETTINGS"]["TELEGRAM_USERS_IDS"])),
            width=self.input_sizes["large"],
        )
        self.telegram_token = self.create_single_input(
            settings,
            "Telegram机器人令牌",
            self.config["SETTINGS"]["TELEGRAM_BOT_TOKEN"],
            width=self.input_sizes["extra_large"],
        )

        # 水龙头分类
        self.create_category_header(left_column, "🚰 水龙头")

        # 创建水龙头设置部分
        faucet = self.create_section(left_column, "水龙头")
        # 创建Capsolver API密钥输入框
        self.capsolver_key = self.create_single_input(
            faucet, "Capsolver API密钥", self.config["FAUCET"]["CAPSOLVER_API_KEY"]
        )

        # 创建分散设置部分
        disperse = self.create_section(left_column, "分散")
        # 创建分散最小余额范围输入框
        self.min_balance_min, self.min_balance_max = self.create_range_inputs(
            disperse,
            "分散最小余额",
            self.config["DISPERSE"]["MIN_BALANCE_FOR_DISPERSE"],
        )

        # 交换分类
        self.create_category_header(left_column, "💱 交换")

        # 创建交换流程设置部分
        flow = self.create_section(left_column, "流程")
        # 创建交换次数范围输入框
        self.swaps_min, self.swaps_max = self.create_range_inputs(
            flow, "交换次数", self.config["FLOW"]["NUMBER_OF_SWAPS"]
        )
        # 创建交换余额百分比范围输入框
        self.balance_swap_min, self.balance_swap_max = self.create_range_inputs(
            flow,
            "交换余额百分比",
            self.config["FLOW"]["PERCENT_OF_BALANCE_TO_SWAP"],
        )

        # NFT分类
        self.create_category_header(left_column, "🎨 NFT")

        # 添加ACCOUNTABLE部分
        accountable = self.create_section(left_column, "ACCOUNTABLE")
        # 创建每个账户NFT限制输入框
        self.accountable_limit = self.create_single_input(
            accountable,
            "每个账户NFT限制",
            self.config["ACCOUNTABLE"]["NFT_PER_ACCOUNT_LIMIT"],
            width=100,
        )

        # 添加LilChogStars部分
        lilchog = self.create_section(left_column, "LilChogStars")
        # 创建每个账户最大数量范围输入框
        self.lilchog_amount_min, self.lilchog_amount_max = self.create_range_inputs(
            lilchog,
            "每个账户最大数量",
            self.config["LILCHOGSTARS"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"],
        )

        # 添加Demask部分
        demask = self.create_section(left_column, "Demask")
        # 创建每个账户最大数量范围输入框
        self.demask_amount_min, self.demask_amount_max = self.create_range_inputs(
            demask,
            "每个账户最大数量",
            self.config["DEMASK"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"],
        )

        # 添加MonadKing部分
        monadking = self.create_section(left_column, "MonadKing")
        # 创建每个账户最大数量范围输入框
        self.monadking_amount_min, self.monadking_amount_max = self.create_range_inputs(
            monadking,
            "每个账户最大数量",
            self.config["MONADKING"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"],
        )

        # 添加MagicEden部分
        magiceden = self.create_section(left_column, "MagicEden")
        # 创建NFT合约列表输入框
        self.magiceden_contracts = self.create_nft_contracts_list(
            magiceden,
            "NFT合约",
            self.config["MAGICEDEN"]["NFT_CONTRACTS"],
        )

        # 右列内容

        # 质押分类
        self.create_category_header(right_column, "🥩 质押")

        # 创建Apriori质押设置部分
        apriori = self.create_section(right_column, "Apriori")
        # 创建Apriori质押数量范围输入框
        self.apriori_stake_min, self.apriori_stake_max = self.create_range_inputs(
            apriori, "质押数量", self.config["APRIORI"]["AMOUNT_TO_STAKE"]
        )

        # 创建Magma质押设置部分
        magma = self.create_section(right_column, "Magma")
        # 创建Magma质押数量范围输入框
        self.magma_stake_min, self.magma_stake_max = self.create_range_inputs(
            magma, "质押数量", self.config["MAGMA"]["AMOUNT_TO_STAKE"]
        )

        # 创建Kintsu质押设置部分
        kintsu = self.create_section(right_column, "Kintsu")
        # 创建Kintsu质押数量范围输入框
        self.kintsu_stake_min, self.kintsu_stake_max = self.create_range_inputs(
            kintsu, "质押数量", self.config["KINTSU"]["AMOUNT_TO_STAKE"]
        )

        # 创建Shmonad质押设置部分
        shmonad = self.create_section(right_column, "Shmonad")
        # 创建购买并质押Shmon复选框
        self.buy_stake = self.create_checkbox(
            shmonad,
            "购买并质押Shmon",
            self.config["SHMONAD"]["BUY_AND_STAKE_SHMON"],
        )
        # 创建取消质押并出售Shmon复选框
        self.unstake_sell = self.create_checkbox(
            shmonad,
            "取消质押并出售Shmon",
            self.config["SHMONAD"]["UNSTAKE_AND_SELL_SHMON"],
        )
        # 创建Shmonad交换余额百分比范围输入框
        self.shmonad_percent_min, self.shmonad_percent_max = self.create_range_inputs(
            shmonad,
            "交换余额百分比",
            self.config["SHMONAD"]["PERCENT_OF_BALANCE_TO_SWAP"],
        )

        # 桥接与GAS分类
        self.create_category_header(right_column, "🌉 桥接与GAS")

        # 添加GasZip部分
        gaszip = self.create_section(right_column, "GasZip")
        # 创建GasZipGAS网络复选框
        self.gaszip_networks = self.create_network_checkboxes(
            gaszip,
            "GAS网络",
            self.config["GASZIP"]["NETWORKS_TO_REFUEL_FROM"],
        )
        # 创建GasZipGAS数量范围输入框
        self.gaszip_amount_min, self.gaszip_amount_max = self.create_range_inputs(
            gaszip, "GAS数量", self.config["GASZIP"]["AMOUNT_TO_REFUEL"]
        )
        # 创建GasZip最小GAS余额输入框
        self.gaszip_min_balance = self.create_single_input(
            gaszip,
            "最小GAS余额",
            self.config["GASZIP"]["MINIMUM_BALANCE_TO_REFUEL"],
            width=self.input_sizes["tiny"],
        )
        # 创建GasZip等待资金到达复选框
        self.gaszip_wait = self.create_checkbox(
            gaszip,
            "等待资金到达",
            self.config["GASZIP"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
        )
        # 创建GasZip最大等待时间输入框
        self.gaszip_wait_time = self.create_single_input(
            gaszip,
            "最大等待时间",
            self.config["GASZIP"]["MAX_WAIT_TIME"],
            width=self.input_sizes["tiny"],
        )

        # 添加MemeBridge部分
        memebridge = self.create_section(right_column, "MemeBridge")
        # 创建MemeBridgeGAS网络复选框
        self.memebridge_networks = self.create_network_checkboxes(
            memebridge,
            "GAS网络",
            self.config["MEMEBRIDGE"]["NETWORKS_TO_REFUEL_FROM"],
        )
        # 创建MemeBridgeGAS数量范围输入框
        self.memebridge_amount_min, self.memebridge_amount_max = (
            self.create_range_inputs(
                memebridge,
                "GAS数量",
                self.config["MEMEBRIDGE"]["AMOUNT_TO_REFUEL"],
            )
        )
        # 创建MemeBridge最小GAS余额输入框
        self.memebridge_min_balance = self.create_single_input(
            memebridge,
            "最小GAS余额",
            self.config["MEMEBRIDGE"]["MINIMUM_BALANCE_TO_REFUEL"],
            width=self.input_sizes["tiny"],
        )
        # 创建MemeBridge等待资金到达复选框
        self.memebridge_wait = self.create_checkbox(
            memebridge,
            "等待资金到达",
            self.config["MEMEBRIDGE"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
        )
        # 创建MemeBridge最大等待时间输入框
        self.memebridge_wait_time = self.create_single_input(
            memebridge,
            "最大等待时间",
            self.config["MEMEBRIDGE"]["MAX_WAIT_TIME"],
            width=self.input_sizes["tiny"],
        )

        # 添加测试网桥接部分
        testnet = self.create_section(right_column, "测试网桥接")
        # 创建测试网桥接GAS网络复选框
        self.testnet_networks = self.create_network_checkboxes(
            testnet,
            "GAS网络",
            self.config["TESTNET_BRIDGE"]["NETWORKS_TO_REFUEL_FROM"],
        )
        # 创建测试网桥接GAS数量范围输入框
        self.testnet_amount_min, self.testnet_amount_max = self.create_range_inputs(
            testnet,
            "GAS数量",
            self.config["TESTNET_BRIDGE"]["AMOUNT_TO_REFUEL"],
        )
        # 创建测试网桥接最小GAS余额输入框
        self.testnet_min_balance = self.create_single_input(
            testnet,
            "最小GAS余额",
            self.config["TESTNET_BRIDGE"]["MINIMUM_BALANCE_TO_REFUEL"],
            width=self.input_sizes["tiny"],
        )
        # 创建测试网桥接等待资金到达复选框
        self.testnet_wait = self.create_checkbox(
            testnet,
            "等待资金到达",
            self.config["TESTNET_BRIDGE"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
        )
        # 创建测试网桥接最大等待时间输入框
        self.testnet_wait_time = self.create_single_input(
            testnet,
            "最大等待时间",
            self.config["TESTNET_BRIDGE"]["MAX_WAIT_TIME"],
            width=self.input_sizes["tiny"],
        )

        # 创建Orbiter桥接设置部分
        orbiter = self.create_section(right_column, "Orbiter")
        # 创建Orbiter桥接数量范围输入框
        self.orbiter_amount_min, self.orbiter_amount_max = self.create_range_inputs(
            orbiter, "桥接数量", self.config["ORBITER"]["AMOUNT_TO_BRIDGE"]
        )
        # 创建Orbiter全部桥接复选框
        self.bridge_all = self.create_checkbox(
            orbiter, "全部桥接", self.config["ORBITER"]["BRIDGE_ALL"]
        )
        # 创建Orbiter等待资金到达复选框
        self.orbiter_wait = self.create_checkbox(
            orbiter,
            "等待资金到达",
            self.config["ORBITER"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
        )
        # 创建Orbiter最大等待时间输入框
        self.orbiter_wait_time = self.create_single_input(
            orbiter, "最大等待时间", self.config["ORBITER"]["MAX_WAIT_TIME"]
        )

    def _save_and_close(self):
        """Save config and close the window"""
        self.save_config()
        self.root.destroy()

    def save_config(self):
        # Update config dictionary with new values
        # SETTINGS
        self.config["SETTINGS"]["THREADS"] = int(self.threads_entry.get())
        self.config["SETTINGS"]["ATTEMPTS"] = int(self.attempts_entry.get())
        self.config["SETTINGS"]["ACCOUNTS_RANGE"] = [
            int(self.acc_range_start.get()),
            int(self.acc_range_end.get()),
        ]

        # Add new SETTINGS fields
        self.config["SETTINGS"]["EXACT_ACCOUNTS_TO_USE"] = [
            int(x.strip()) for x in self.exact_accounts.get().split(",") if x.strip()
        ]

        # Паузы в секундах (целые числа)
        self.config["SETTINGS"]["PAUSE_BETWEEN_ATTEMPTS"] = [
            int(float(self.pause_attempts_min.get())),
            int(float(self.pause_attempts_max.get())),
        ]
        self.config["SETTINGS"]["PAUSE_BETWEEN_SWAPS"] = [
            int(float(self.pause_swaps_min.get())),
            int(float(self.pause_swaps_max.get())),
        ]
        self.config["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACCOUNTS"] = [
            int(float(self.pause_accounts_min.get())),
            int(float(self.pause_accounts_max.get())),
        ]
        self.config["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACTIONS"] = [
            int(float(self.pause_actions_min.get())),
            int(float(self.pause_actions_max.get())),
        ]
        self.config["SETTINGS"]["RANDOM_INITIALIZATION_PAUSE"] = [
            int(float(self.init_pause_min.get())),
            int(float(self.init_pause_max.get())),
        ]

        self.config["SETTINGS"]["BROWSER_PAUSE_MULTIPLIER"] = float(
            self.browser_multiplier.get()
        )

        self.config["SETTINGS"]["TELEGRAM_USERS_IDS"] = [
            int(x.strip()) for x in self.telegram_ids.get().split(",") if x.strip()
        ]
        self.config["SETTINGS"]["TELEGRAM_BOT_TOKEN"] = self.telegram_token.get()

        # FLOW
        self.config["FLOW"]["NUMBER_OF_SWAPS"] = [
            int(float(self.swaps_min.get())),
            int(float(self.swaps_max.get())),
        ]
        self.config["FLOW"]["PERCENT_OF_BALANCE_TO_SWAP"] = [
            int(float(self.balance_swap_min.get())),
            int(float(self.balance_swap_max.get())),
        ]

        # FAUCET
        self.config["FAUCET"]["CAPSOLVER_API_KEY"] = self.capsolver_key.get()

        # DISPERSE
        self.config["DISPERSE"]["MIN_BALANCE_FOR_DISPERSE"] = [
            float(self.min_balance_min.get()),
            float(self.min_balance_max.get()),
        ]

        # APRIORI
        self.config["APRIORI"]["AMOUNT_TO_STAKE"] = [
            float(self.apriori_stake_min.get()),
            float(self.apriori_stake_max.get()),
        ]

        # MAGMA
        self.config["MAGMA"]["AMOUNT_TO_STAKE"] = [
            float(self.magma_stake_min.get()),
            float(self.magma_stake_max.get()),
        ]

        # KINTSU
        self.config["KINTSU"]["AMOUNT_TO_STAKE"] = [
            float(self.kintsu_stake_min.get()),
            float(self.kintsu_stake_max.get()),
        ]

        # GASZIP
        self.config["GASZIP"]["NETWORKS_TO_REFUEL_FROM"] = [
            network for network, var in self.gaszip_networks if var.get()
        ]
        self.config["GASZIP"]["AMOUNT_TO_REFUEL"] = [
            float(self.gaszip_amount_min.get()),
            float(self.gaszip_amount_max.get()),
        ]
        self.config["GASZIP"]["MINIMUM_BALANCE_TO_REFUEL"] = float(
            self.gaszip_min_balance.get()
        )
        self.config["GASZIP"]["WAIT_FOR_FUNDS_TO_ARRIVE"] = self.gaszip_wait.get()
        self.config["GASZIP"]["MAX_WAIT_TIME"] = int(self.gaszip_wait_time.get())

        # MEMEBRIDGE
        self.config["MEMEBRIDGE"]["NETWORKS_TO_REFUEL_FROM"] = [
            network for network, var in self.memebridge_networks if var.get()
        ]
        self.config["MEMEBRIDGE"]["AMOUNT_TO_REFUEL"] = [
            float(self.memebridge_amount_min.get()),
            float(self.memebridge_amount_max.get()),
        ]
        self.config["MEMEBRIDGE"]["MINIMUM_BALANCE_TO_REFUEL"] = float(
            self.memebridge_min_balance.get()
        )
        self.config["MEMEBRIDGE"][
            "WAIT_FOR_FUNDS_TO_ARRIVE"
        ] = self.memebridge_wait.get()
        self.config["MEMEBRIDGE"]["MAX_WAIT_TIME"] = int(
            self.memebridge_wait_time.get()
        )

        # TESTNET_BRIDGE
        self.config["TESTNET_BRIDGE"]["NETWORKS_TO_REFUEL_FROM"] = [
            network for network, var in self.testnet_networks if var.get()
        ]
        self.config["TESTNET_BRIDGE"]["AMOUNT_TO_REFUEL"] = [
            float(self.testnet_amount_min.get()),
            float(self.testnet_amount_max.get()),
        ]
        self.config["TESTNET_BRIDGE"]["MINIMUM_BALANCE_TO_REFUEL"] = float(
            self.testnet_min_balance.get()
        )
        self.config["TESTNET_BRIDGE"][
            "WAIT_FOR_FUNDS_TO_ARRIVE"
        ] = self.testnet_wait.get()
        self.config["TESTNET_BRIDGE"]["MAX_WAIT_TIME"] = int(
            self.testnet_wait_time.get()
        )

        # ACCOUNTABLE
        self.config["ACCOUNTABLE"]["NFT_PER_ACCOUNT_LIMIT"] = int(
            self.accountable_limit.get()
        )

        # LILCHOGSTARS
        self.config["LILCHOGSTARS"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"] = [
            int(self.lilchog_amount_min.get()),
            int(self.lilchog_amount_max.get()),
        ]

        # DEMASK
        self.config["DEMASK"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"] = [
            int(self.demask_amount_min.get()),
            int(self.demask_amount_max.get()),
        ]

        # MONADKING
        self.config["MONADKING"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"] = [
            int(self.monadking_amount_min.get()),
            int(self.monadking_amount_max.get()),
        ]

        # MAGICEDEN
        self.config["MAGICEDEN"]["NFT_CONTRACTS"] = [
            x.strip()
            for x in self.magiceden_contracts.get("1.0", "end-1c").split("\n")
            if x.strip()
        ]

        # SHMONAD
        self.config["SHMONAD"]["BUY_AND_STAKE_SHMON"] = self.buy_stake.get()
        self.config["SHMONAD"]["UNSTAKE_AND_SELL_SHMON"] = self.unstake_sell.get()
        self.config["SHMONAD"]["PERCENT_OF_BALANCE_TO_SWAP"] = [
            int(float(self.shmonad_percent_min.get())),
            int(float(self.shmonad_percent_max.get())),
        ]

        # ORBITER
        self.config["ORBITER"]["AMOUNT_TO_BRIDGE"] = [
            float(self.orbiter_amount_min.get()),
            float(self.orbiter_amount_max.get()),
        ]
        self.config["ORBITER"]["BRIDGE_ALL"] = self.bridge_all.get()
        self.config["ORBITER"]["WAIT_FOR_FUNDS_TO_ARRIVE"] = self.orbiter_wait.get()
        self.config["ORBITER"]["MAX_WAIT_TIME"] = int(self.orbiter_wait_time.get())

        # Save to file
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.yaml")
        with open(config_path, "w") as file:
            yaml.dump(self.config, file, default_flow_style=False)

    def run(self):
        """Run the configuration UI"""
        self.root.mainloop()


# Удалить или закомментировать эту часть, так как теперь запуск будет через метод run()
# def main():
#     app = ConfigUI()
#     app.root.mainloop()


# if __name__ == "__main__":
#     main()
