
let elements = {};

// ============================================
// مقداردهی اولیه
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    elements = {
        methodRadios: document.querySelectorAll('input[name="method"]'),
        toolSelect: document.getElementById('toolSelect'),
        toolInfo: document.getElementById('toolInfo'),
        scenarioSelect: document.getElementById('scenarioSelect'),
        scenarioInfo: document.getElementById('scenarioInfo'),
        submitBtn: document.getElementById('submitBtn'),
        loadingArea: document.getElementById('loadingArea'),
        resultBox: document.getElementById('resultBox'),
        outputText: document.getElementById('outputText'),
        explanationText: document.getElementById('explanationText'),
        scenarioCodeText: document.getElementById('scenarioCodeText'),
        copyScenarioBtn: document.getElementById('copyScenarioBtn')
    };
    
    elements.methodRadios.forEach(radio => {
        radio.addEventListener('change', onMethodChange);
    });
    
    elements.toolSelect.addEventListener('change', onToolChange);
    elements.scenarioSelect.addEventListener('change', onScenarioChange);
    
    updateToolsList();
    updateScenariosList();
    updateToolInfo();
    updateScenarioInfo();
    updateScenarioCode();
    
    console.log('✅ صفحه بارگذاری شد');
});

// ============================================
// توابع تغییر روش
// ============================================

function onMethodChange() {
    updateToolsList();
    updateScenariosList();
    updateToolInfo();
    updateScenarioInfo();
    updateScenarioCode();
}

function getSelectedMethod() {
    let selected = 'thread';
    elements.methodRadios.forEach(radio => {
        if (radio.checked) selected = radio.value;
    });
    return selected;
}

// ============================================
// توابع به‌روزرسانی ابزارها
// ============================================

function updateToolsList() {
    const method = getSelectedMethod();
    const tools = method === 'thread' ? THREAD_TOOLS : PROCESS_TOOLS;
    const previousValue = elements.toolSelect.value;
    
    elements.toolSelect.innerHTML = '';
    tools.forEach(tool => {
        const option = document.createElement('option');
        option.value = tool.id;
        option.textContent = tool.name;
        elements.toolSelect.appendChild(option);
    });
    
    if (previousValue && tools.some(t => t.id === previousValue)) {
        elements.toolSelect.value = previousValue;
    }
}

function updateToolInfo() {
    const method = getSelectedMethod();
    const tools = method === 'thread' ? THREAD_TOOLS : PROCESS_TOOLS;
    const selectedTool = tools.find(t => t.id === elements.toolSelect.value);
    if (selectedTool) {
        elements.toolInfo.innerHTML = `<i>📖</i> ${selectedTool.desc}`;
    }
}

function onToolChange() {
    updateToolInfo();
    updateScenariosList();
    updateScenarioInfo();
    updateScenarioCode();
}

// ============================================
// توابع به‌روزرسانی سناریوها
// ============================================

function updateScenariosList() {
    const method = getSelectedMethod();
    const toolId = elements.toolSelect.value;
    const scenarios = (method === 'thread') ? SCENARIOS[toolId] : null;
    
    elements.scenarioSelect.innerHTML = '';
    
    if (scenarios) {
        for (let i = 1; i <= 3; i++) {
            if (scenarios[i]) {
                const option = document.createElement('option');
                option.value = i;
                option.textContent = scenarios[i].name;
                elements.scenarioSelect.appendChild(option);
            }
        }
    } else {
        for (let i = 1; i <= 3; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `سناریو ${i}: در حال توسعه`;
            elements.scenarioSelect.appendChild(option);
        }
    }
}

function updateScenarioInfo() {
    const method = getSelectedMethod();
    const toolId = elements.toolSelect.value;
    const scenarioId = parseInt(elements.scenarioSelect.value);
    
    let isAvailable = false;
    let scenarioDesc = 'این سناریو در حال توسعه است';
    
    if (method === 'thread' && SCENARIOS[toolId] && SCENARIOS[toolId][scenarioId]) {
        scenarioDesc = SCENARIOS[toolId][scenarioId].desc;
        isAvailable = true;
    }
    
    elements.scenarioInfo.innerHTML = `<i>${isAvailable ? '📖' : '⏳'}</i> ${scenarioDesc}`;
    elements.submitBtn.disabled = !isAvailable;
}

function onScenarioChange() {
    updateScenarioInfo();
    updateScenarioCode();
}

// ============================================
// نمایش کد سناریو (با هایلایت)
// ============================================

function updateScenarioCode() {
    const toolId = elements.toolSelect.value;
    const scenarioId = parseInt(elements.scenarioSelect.value);
    
    let code = (SCENARIO_CODES[toolId] && SCENARIO_CODES[toolId][scenarioId])
        ? SCENARIO_CODES[toolId][scenarioId]
        : '# این سناریو در حال توسعه است\n# به زودی کد آن اضافه می‌شود';
    
    elements.scenarioCodeText.innerHTML = code;
}
// ============================================
// کپی کد (بدون تگ‌های HTML)
// ============================================

function copyScenarioCode() {
    const toolId = elements.toolSelect.value;
    const scenarioId = parseInt(elements.scenarioSelect.value);
    
    // گرفتن کد خام (بدون HTML)
    let code = (SCENARIO_CODES[toolId] && SCENARIO_CODES[toolId][scenarioId])
        ? SCENARIO_CODES[toolId][scenarioId]
        : '# این سناریو در حال توسعه است\n# به زودی کد آن اضافه می‌شود';
    
    navigator.clipboard.writeText(code).then(() => {
        if (elements.copyScenarioBtn) {
            const original = elements.copyScenarioBtn.textContent;
            elements.copyScenarioBtn.textContent = '✅ کپی شد!';
            elements.copyScenarioBtn.classList.add('copied');
            setTimeout(() => {
                elements.copyScenarioBtn.textContent = original;
                elements.copyScenarioBtn.classList.remove('copied');
            }, 2000);
        }
    }).catch(err => {
        console.error('خطا در کپی:', err);
    });
}

// ============================================
// اجرای سناریو
// ============================================

async function runScenario() {
    const method = getSelectedMethod();
    const toolId = elements.toolSelect.value;
    const scenarioId = parseInt(elements.scenarioSelect.value);
    
    if (method === 'thread' && (!SCENARIOS[toolId] || !SCENARIOS[toolId][scenarioId])) {
        alert('این سناریو در حال توسعه است');
        return;
    }
    
    elements.resultBox.style.display = 'none';
    elements.loadingArea.style.display = 'block';
    elements.submitBtn.disabled = true;
    
    try {
        const response = await fetch(`/${method}/${toolId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario_id: scenarioId })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'خطا در ارتباط با سرور');
        }
        
        const data = await response.json();
        
        elements.outputText.textContent = data.output || 'خروجی دریافت نشد';
        elements.explanationText.textContent = data.explanation || 'توضیحاتی موجود نیست';
        elements.resultBox.style.display = 'block';
        
    } catch (error) {
        elements.outputText.textContent = `❌ خطا: ${error.message}`;
        elements.explanationText.textContent = 'مشکلی در اجرای درخواست پیش آمد.';
        elements.resultBox.style.display = 'block';
    } finally {
        elements.loadingArea.style.display = 'none';
        elements.submitBtn.disabled = false;
    }
}