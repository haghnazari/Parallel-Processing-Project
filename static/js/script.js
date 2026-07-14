const App = {

    elements: {},

    init() {

        this.cacheElements();
        this.bindEvents();

        this.refreshUI();

        console.log("✅ Application Loaded");
    },

    // ==================================================
    // Elements
    // ==================================================

    cacheElements() {

        this.elements = {

            methodRadios:
                document.querySelectorAll('input[name="method"]'),

            toolSelect:
                document.getElementById("toolSelect"),

            toolInfo:
                document.getElementById("toolInfo"),

            scenarioSelect:
                document.getElementById("scenarioSelect"),

            scenarioInfo:
                document.getElementById("scenarioInfo"),

            submitBtn:
                document.getElementById("submitBtn"),

            loadingArea:
                document.getElementById("loadingArea"),

            resultBox:
                document.getElementById("resultBox"),

            outputText:
                document.getElementById("outputText"),

            explanationText:
                document.getElementById("explanationText")
        };
    },

    // ==================================================
    // Events
    // ==================================================

    bindEvents() {

        this.elements.methodRadios.forEach(radio => {
            radio.addEventListener(
                "change",
                () => this.refreshUI()
            );
        });

        this.elements.toolSelect.addEventListener(
            "change",
            () => {

                this.updateToolInfo();
                this.updateScenarioList();
                this.updateScenarioInfo();
            }
        );

        this.elements.scenarioSelect.addEventListener(
            "change",
            () => {

                this.updateScenarioInfo();
            }
        );
    },

    // ==================================================
    // Refresh
    // ==================================================

    refreshUI() {

        this.updateToolList();
        this.updateToolInfo();

        this.updateScenarioList();
        this.updateScenarioInfo();
    },

    // ==================================================
    // Helpers
    // ==================================================

    getMethod() {

        let value = "thread";

        this.elements.methodRadios.forEach(radio => {

            if (radio.checked)
                value = radio.value;
        });

        return value;
    },

    getTools() {

        return this.getMethod() === "thread"
            ? THREAD_TOOLS
            : PROCESS_TOOLS;
    },

    // ==================================================
    // Tool Section
    // ==================================================

    updateToolList() {

        const tools = this.getTools();

        const previous =
            this.elements.toolSelect.value;

        this.elements.toolSelect.innerHTML = "";

        tools.forEach(tool => {

            const option =
                document.createElement("option");

            option.value = tool.id;
            option.textContent = tool.name;

            this.elements.toolSelect.appendChild(option);
        });

        if (
            previous &&
            tools.some(t => t.id === previous)
        ) {
            this.elements.toolSelect.value = previous;
        }
    },

    updateToolInfo() {

        const tools = this.getTools();

        const selectedTool =
            tools.find(
                t => t.id ===
                this.elements.toolSelect.value
            );

        if (!selectedTool)
            return;

        this.elements.toolInfo.innerHTML =
            `📖 ${selectedTool.desc}`;
    },

    // ==================================================
    // Scenario Section
    // ==================================================

    updateScenarioList() {
    const toolId = this.elements.toolSelect.value;
    const method = this.getMethod();
    let scenarios = null;

    // تفکیک مطلق بر اساس متد انتخابی کاربر
    if (method === "thread") {
        scenarios = THREAD_SCENARIOS[toolId] || {};
    } else {
        scenarios = PROCESS_SCENARIOS[toolId] || {};
    }

    this.elements.scenarioSelect.innerHTML = "";
    const totalScenarios = Object.keys(scenarios).length;

    if (totalScenarios === 0) {
        // اگر هیچ سناریویی یافت نشد، دکمه یا آپشن خالی نمایش داده شود
        const option = document.createElement("option");
        option.value = "";
        option.textContent = "هیچ سناریویی یافت نشد";
        this.elements.scenarioSelect.appendChild(option);
        return;
    }

    for (let i = 1; i <= totalScenarios; i++) {
        const option = document.createElement("option");
        option.value = i;

        if (scenarios[i]) {
            option.textContent = scenarios[i].name;
        } else {
            option.textContent = `سناریو ${i} (در حال توسعه)`;
        }

        this.elements.scenarioSelect.appendChild(option);
    }
},

    updateScenarioInfo() {
    const toolId = this.elements.toolSelect.value;
    const scenarioId = parseInt(this.elements.scenarioSelect.value);
    const method = this.getMethod();

    let available = false;
    let description = "این سناریو در حال توسعه است.";

    // بررسی دقیق ساختار تردها
    if (method === "thread") {
        if (THREAD_SCENARIOS[toolId] && THREAD_SCENARIOS[toolId][scenarioId]) {
            available = true;
            description = THREAD_SCENARIOS[toolId][scenarioId].desc;
        }
    } 
    // بررسی دقیق ساختار فرآیندها
    else if (method === "process") {
        if (PROCESS_SCENARIOS[toolId] && PROCESS_SCENARIOS[toolId][scenarioId]) {
            available = true;
            description = PROCESS_SCENARIOS[toolId][scenarioId].desc;
        }
    }

    this.elements.scenarioInfo.innerHTML = available
        ? `📖 ${description}`
        : `⏳ ${description}`;

    // دکمه ارسال فقط در صورت معتبر بودن سناریو و شناسه فعال شود
    this.elements.submitBtn.disabled = !available || isNaN(scenarioId);
},

    // ==================================================
    // Loading
    // ==================================================

    showLoading() {

        this.elements.loadingArea.style.display =
            "block";

        this.elements.submitBtn.disabled = true;
    },

    hideLoading() {

        this.elements.loadingArea.style.display =
            "none";

        this.updateScenarioInfo();
    },

    // ==================================================
    // Result
    // ==================================================

    showResult(output, explanation) {

        this.elements.outputText.textContent =
            output;

        this.elements.explanationText.textContent =
            explanation;

        this.elements.resultBox.style.display =
            "block";

        this.elements.resultBox.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    },

    showError(message) {

        this.showResult(
            `❌ ${message}`,
            "اجرای سناریو با خطا مواجه شد."
        );
    }
};

// ======================================================
// Execute Scenario
// ======================================================

async function runScenario() {

    const method =
        App.getMethod();

    const tool =
        App.elements.toolSelect.value;

    const scenario =
        parseInt(
            App.elements.scenarioSelect.value
        );

    App.showLoading();

    App.elements.resultBox.style.display =
        "none";

    try {

        const response =
            await fetch(
                `/${method}/${tool}`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        scenario_id: scenario
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Server Error"
            );
        }

        App.showResult(
            data.output || "",
            data.explanation || ""
        );

    }
    catch (error) {

        console.error(error);

        App.showError(
            error.message
        );
    }
    finally {

        App.hideLoading();
    }
}

// ======================================================
// Startup
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    () => App.init()
);
