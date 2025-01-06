/**
 * Hàm chung để ẩn/hiện nội dung và điều chỉnh biểu tượng mũi tên.
 * @param {string} contentId - ID của phần tử nội dung cần ẩn/hiện.
 * @param {string} arrowId - ID của biểu tượng mũi tên cần xoay.
 */

let sidebarOpen = false;
let gender = "";

function showAlert(message) {
    const alertBox = document.getElementById("custom-alert");
    const alertMessage = document.getElementById("alert-message");
    alertMessage.textContent = message;
    alertBox.classList.remove('hide');
    alertBox.classList.add('show'); 
    alertBox.style.display = "block";
}

function closeAlert() {
    const alertBox = document.getElementById("custom-alert");
    const dobInput = document.getElementById("dob"); 
    alertBox.classList.remove('show'); // Loại bỏ class `show` nếu có
    alertBox.classList.add('hide');    // Thêm class `hide` để áp dụng hiệu ứng Zoom Out

    // Đợi 0.25s (thời gian của hiệu ứng zoomOut) rồi ẩn modal
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 250);
    dobInput.value = ""; //Reset lại DOB - buộc người dùng phải chọn lại
}

function toggleAgeInput() {
    const selectedOption = document.getElementById("age-option").value;
    const dobFlatpickr = document.querySelector("#dob")._flatpickr;
    // Reset required attributes
    document.getElementById("dob").required = false;
    document.getElementById("current-day").required = false;
    document.getElementById("age-months").required = false;
    document.getElementById("age-days").required = false;

    document.getElementById("age-days").value = ""; 
    document.getElementById("age-months").value = "";

    if (selectedOption === "dob") {
        document.getElementById("dob-container").style.display = "flex";
        document.getElementById("months-input").style.display = "none";
        document.getElementById("days-input").style.display = "none";
        document.getElementById("age-display").innerHTML = "";
        // Reset giá trị dob
        if (dobFlatpickr) {
            dobFlatpickr.clear();
        }
        document.getElementById("dob").required = true;
        document.getElementById("current-day").required = true;
        document.getElementById("age-months-error").style.display = "none";
        document.querySelector(".age-months-group")?.classList.remove("error-border");
        document.getElementById("age-days-error").style.display = "none";
        document.querySelector(".age-days-group")?.classList.remove("error-border");
    } else if (selectedOption === "months") {
        document.getElementById("dob-container").style.display = "none";
        document.getElementById("months-input").style.display = "block";
        document.getElementById("days-input").style.display = "none";
        document.getElementById("age-display").innerHTML = "";
        document.getElementById("dob-error").style.display = "none";
        document.querySelector(".input-row")?.classList.remove("error-border");
        document.getElementById("age-days-error").style.display = "none";
        document.querySelector(".age-days-group")?.classList.remove("error-border");
    } else if (selectedOption === "days") {
        document.getElementById("dob-container").style.display = "none";
        document.getElementById("months-input").style.display = "none";
        document.getElementById("days-input").style.display = "block";
        document.getElementById("age-display").innerHTML = "";
        document.getElementById("dob-error").style.display = "none";
        document.querySelector(".input-row")?.classList.remove("error-border");
        document.getElementById("age-months-error").style.display = "none";
        document.querySelector(".age-months-group")?.classList.remove("error-border");
    }
}

function toggleCollapse(contentId, arrowId) {
    const content = document.getElementById(contentId);
    const arrow = document.getElementById(arrowId);

    if (content) {
        // Kiểm tra trạng thái mở rộng
        if (!content.classList.contains('expand')) {
            content.style.maxHeight = content.scrollHeight + "px"; // Chiều cao tự động
        } else {
            content.style.maxHeight = null; // Reset maxHeight
        }
        content.classList.toggle('expand');

        // Xoay mũi tên
        if (arrow) {
            arrow.style.transform = content.classList.contains('expand')
                ? 'rotate(180deg)'
                : 'rotate(0deg)';
        }
    }
}

function observeContentChanges(contentId) {
    const content = document.getElementById(contentId);

    if (content) {
        const observer = new MutationObserver(() => {
            if (content.classList.contains('expand')) {
                // Cập nhật maxHeight khi nội dung thay đổi
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });

        observer.observe(content, { childList: true, subtree: true, characterData: true });
    }
}

// Hàm tính ageInDays dựa trên phương pháp nhập liệu
function calculateAgeInDaysFromOption(selectedOption) {
    let ageInDays;
    if (selectedOption === "dob") {
        const dob = document.getElementById("dob").value;
        const currentDay = document.getElementById("current-day").value;
        if (dob && currentDay) {
            ageInDays = calculateAgeInDays(dob, currentDay);
        }
    } else if (selectedOption === "months") {
        const ageMonths = parseInt(document.getElementById("age-months").value, 10);
        if (!isNaN(ageMonths)) {
            ageInDays = ageMonths * 30.4375;
        }
    } else if (selectedOption === "days") {
        const ageDays = parseInt(document.getElementById("age-days").value, 10);
        if (!isNaN(ageDays)) {
            ageInDays = ageDays;
        }
    }

    return ageInDays;
}

function toggleSidebar() {
    const sidebar = document.getElementById("mySidebar");
    const tooltip = document.querySelector(".tooltip-text");
    const iconContainer = document.querySelector(".icon-container");
    const overlay = document.getElementById("myOverlay");

    if (sidebarOpen) {
        tooltip.textContent = "Mở Sidebar";
        document.body.classList.remove("sidebar-open");
        sidebarOpen = false;
    } else {
        tooltip.textContent = "Đóng Sidebar";
        tooltip.style.visibility = "hidden";
        document.body.classList.add("sidebar-open");
        sidebarOpen = true;
    }

    // Hiển thị/ẩn overlay
    overlay.style.display = sidebarOpen ? "block" : "none";

    // Khi hover lại icon, tooltip sẽ hiện lại
    iconContainer.onmouseover = function () {
        tooltip.style.visibility = "visible";
    };
}
function validateFiO2() {
    const fio2Input = document.getElementById("fio2").value;
    const totalFlowInput = document.getElementById("totalFlow").value;

    // Kiểm tra FiO2 có hợp lệ hay không
    if (fio2Input < 21 || fio2Input > 100) {
        alert("FiO2 phải nằm trong khoảng từ 21 đến 100%. Vui lòng nhập lại.");
        document.getElementById("airFlow").value = "";
        document.getElementById("oxyFlow").value = "";
        return false; // Ngăn không cho form submit hoặc tính toán
    }
    calculateFlow();
    return false;
}
function calculateFlow() {
    const fio2 = parseFloat(document.getElementById("fio2").value);
    const totalFlow = parseFloat(document.getElementById("totalFlow").value);

    // Hiển thị cảnh báo nếu FiO2 > 80%
    const warningMessage = document.getElementById("warningMessage");
    if (fio2 > 80) {
        warningMessage.textContent =
            "Warning: FiO2 value should not exceed 80%!";
    } else {
        warningMessage.textContent = "";
    }

    if (isNaN(fio2) || isNaN(totalFlow)) {
        alert("Please enter valid FiO2 and Total Flow values.");
        return;
    }

    // Công thức tính Air Flow và Oxy Flow
    const airFlow = totalFlow - (fio2 * totalFlow - 21 * totalFlow) / 79;
    const oxyFlow = totalFlow - airFlow;

    // Hiển thị kết quả
    document.getElementById("airFlow").textContent = "Air Flow: " + airFlow.toFixed(2) + " L/min";
    document.getElementById("oxyFlow").textContent = "Oxy Flow: " + oxyFlow.toFixed(2) + " L/min";
}

function loadPage(page) {
    fetch(page)
        .then((response) => response.text())
        .then((data) => {
            document.getElementById("main").innerHTML = data;
            // Lưu lại trang hiện tại vào localStorage
            sessionStorage.setItem("lastPage", page);
        })
        .catch((error) => {
            console.error("Error loading page:", error);
        });
}
// Hàm để tải lại trang cuối cùng khi tải lại trang web
function loadLastPage() {
    // Kiểm tra xem trang cuối cùng đã được lưu trong localStorage hay chưa
    var lastPage = sessionStorage.getItem("lastPage");
    if (lastPage) {
        loadPage(lastPage);
    } else {
        // Nếu không có, mặc định tải trang cpap.html
        loadPage("cpap.html");
    }

    // Kiểm tra xem mục được chọn cuối cùng đã được lưu trong localStorage hay chưa
    var selectedItem = sessionStorage.getItem("selectedItem");
    if (selectedItem) {
        highlightSelected(selectedItem);
    } else {
        // Nếu không có, mặc định chọn mục đầu tiên (item1)
        highlightSelected("item1");
    }
}

function highlightSelected(selectedId) {
    // Xóa lớp "selected" từ các mục khác
    var items = document.querySelectorAll(".sidebar a");
    items.forEach(function (item) {
        item.classList.remove("selected");
    });

    // Thêm lớp "selected" cho mục đang được chọn
    var selectedItem = document.getElementById(selectedId);
    selectedItem.classList.add("selected");

    // Lưu lại mục được chọn vào localStorage
    sessionStorage.setItem("selectedItem", selectedId);
}

function calculateETT() {
    const age = parseInt(document.getElementById("ageInput").value);

    // Kiểm tra giá trị của tuổi trong khoảng từ 1 đến 12
    if (age < 1 || age > 12 || isNaN(age)) {
        alert("Vui lòng nhập tuổi hợp lệ từ 1 đến 12.");
        return;
    }

    // Tính toán NKQ không bóng và có bóng
    const ettWithoutCuff = age / 4 + 4;
    const ettWithCuff = age / 4 + 3.5;

    // Tính toán độ sâu nội khí quản
    const ettDepth = ettWithCuff * 3; // Công thức tính độ sâu: ETT với bóng * 3
    document.getElementById("age").textContent = age;
    // Hiển thị kết quả
    document.getElementById("ettWithoutCuff").textContent = ettWithoutCuff.toFixed(1) + " mm";
    document.getElementById("ettWithCuff").textContent = ettWithCuff.toFixed(1) + " mm";
    document.getElementById("ettDepth").textContent = ettDepth.toFixed(1) + " cm";

    // Ẩn form nhập liệu và hiện kết quả
    document.getElementById("formBox").style.display = "none";
    document.getElementById("resultBoxes").style.display = "block";
    document.getElementById("resetBtn").style.display = "inline-block";
}

function resetForm() {
    // Ẩn kết quả và hiển thị lại form nhập liệu
    document.getElementById("resultBoxes").style.display = "none";
    document.getElementById("resetBtn").style.display = "none";
    document.getElementById("formBox").style.display = "block";

    // Reset giá trị của form
    document.getElementById("ageInput").value = "";
}

function calculateBMIandBSA() {
    var weight = document.getElementById("weight").value;
    var height = document.getElementById("height").value;
    // Kiểm tra xem các trường có để trống hay không
    if (!weight || !height) {
        warningMessage.textContent =
            "Warning: Please enter both weight and height.";
        // Ẩn kết quả nếu chưa nhập đủ dữ liệu
        document.getElementById("resultBoxBMI").style.display = "none";
        document.getElementById("text1").style.display = "block"; // Hiển thị placeholder
        return;
    } else {
        warningMessage.textContent = "";
    }
    if (weight && height) {
        // Tính BMI
        var heightInMeters = height / 100; // Chuyển đổi chiều cao từ cm sang mét
        var bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1); // Tính BMI và làm tròn

        var bmiCategory = "";
        if (bmi < 18.5) {
            bmiCategory = "Underweight";
        } else if (bmi >= 18.5 && bmi <= 24.9) {
            bmiCategory = "Normal weight";
        } else if (bmi >= 25 && bmi <= 29.9) {
            bmiCategory = "Overweight";
        } else if (bmi >= 30 && bmi <= 34.9) {
            bmiCategory = "Obese (Class 1)";
        } else if (bmi >= 35 && bmi <= 39.9) {
            bmiCategory = "Obese (Class 2)";
        } else {
            bmiCategory = "Obese (Class 3)";
        }

        document.getElementById("bmi-output").innerHTML = `${bmi} kg/m²`;
        document.getElementById("bmiCategory-output").innerHTML =
            `${bmiCategory}`;
        // Tính BSA sử dụng công thức Mosteller
        var bsa = Math.sqrt((weight * height) / 3600).toFixed(2); // Tính BSA và làm tròn
        document.getElementById("bsa-output").innerHTML = `${bsa} m²`;
    } else {
        document.getElementById("bmi-output").innerHTML =
            "Please fill out required fields.";
        document.getElementById("bsa-output").innerHTML = "";
    }

    document.getElementById("text1").style.display = "none"; // Ẩn placeholder
    document.getElementById("resultBoxBMI").style.display = "flex"; // Hiển thị kết quả
}

// JavaScript functions

function toggleUnit(fieldId, labelId) {
    const inputField = document.getElementById(fieldId);
    const label = document.getElementById(labelId);
    let value = parseFloat(inputField.value);

    // Toggle unit in the label
    if (inputField.dataset.unit === "g/L") {
        inputField.dataset.unit = "g/dL";
        label.textContent = label.textContent.replace("g/L", "g/dL");

        // Convert value only if it's not empty
        if (!isNaN(value)) {
            inputField.value = (value / 10).toFixed(2); // Convert to g/dL
        }
    } else {
        inputField.dataset.unit = "g/L";
        label.textContent = label.textContent.replace("g/dL", "g/L");

        // Convert value only if it's not empty
        if (!isNaN(value)) {
            inputField.value = (value * 10).toFixed(2); // Convert to g/L
        }
    }
}

// Set initial data-unit for conversion
document.getElementById("serumProtein").dataset.unit = "g/dL";
document.getElementById("pleuralFluidProtein").dataset.unit = "g/dL";

function calculateLightCriteria() {
    const serumProteinInput = document.getElementById("serumProtein");
    const pleuralFluidProteinInput = document.getElementById(
        "pleuralFluidProtein",
    );
    const serumLDH = parseFloat(document.getElementById("serumLDH").value);
    const pleuralFluidLDH = parseFloat(
        document.getElementById("pleuralFluidLDH").value,
    );
    const upperLimitLDH = parseFloat(
        document.getElementById("upperLimitLDH").value,
    );

    let serumProtein = parseFloat(serumProteinInput.value);
    let pleuralFluidProtein = parseFloat(pleuralFluidProteinInput.value);

    // Check if serum and pleural fluid proteins are in the same unit
    if (
        serumProteinInput.dataset.unit !== pleuralFluidProteinInput.dataset.unit
    ) {
        // Convert pleural fluid protein to match serum protein unit
        if (
            serumProteinInput.dataset.unit === "g/dL" &&
            pleuralFluidProteinInput.dataset.unit === "g/L"
        ) {
            pleuralFluidProtein /= 10; // Convert from g/L to g/dL
        } else if (
            serumProteinInput.dataset.unit === "g/L" &&
            pleuralFluidProteinInput.dataset.unit === "g/dL"
        ) {
            pleuralFluidProtein *= 10; // Convert from g/dL to g/L
        }
    }

    if (
        isNaN(serumProtein) ||
        isNaN(pleuralFluidProtein) ||
        isNaN(serumLDH) ||
        isNaN(pleuralFluidLDH) ||
        isNaN(upperLimitLDH)
    ) {
        document.getElementById("warningMessage").textContent =
            "Warning: Please enter all values.";
        return;
    } else {
        warningMessage.textContent = "";
    }

    const criteria1 = pleuralFluidProtein / serumProtein > 0.5;
    const criteria2 = pleuralFluidLDH / serumLDH > 0.6;
    const criteria3 = pleuralFluidLDH > (2 / 3) * upperLimitLDH;

    const criteriaMet = [criteria1, criteria2, criteria3].filter(
        Boolean,
    ).length;
    const result =
        criteria1 || criteria2 || criteria3
            ? "Exudative Effusion"
            : "Transudative Effusion";
    document.getElementById("resultLight").innerHTML =
        `${result} (Criteria Met: ${criteriaMet}/3)`;
    document.getElementById("text1").style.display = "none";
    document.getElementById("resultBoxLight").style.display = "flex";
}

function selectGender(selectedGender) {
    gender = selectedGender;
    // Xóa trạng thái "active" khỏi cả hai nút
    document.getElementById("male-btn").classList.remove("active");
    document.getElementById("female-btn").classList.remove("active");

    // Thêm trạng thái "active" cho nút được chọn
    if (selectedGender === "male") {
        document.getElementById("male-btn").classList.add("active");
    } else {
        document.getElementById("female-btn").classList.add("active");
    }
    // Cập nhật giá trị trường ẩn với giới tính đã chọn
    document.getElementById("gender").value = gender;
    // Ẩn thông báo lỗi khi chọn giới tính
    document.getElementById("gender-error").style.display = "none";
    // Xóa hiệu ứng viền đỏ của khung chọn giới tính
    document.getElementById("gender-select-group").classList.remove("error-border");
}


function selectMeasured(measured) {
    document.getElementById("measured").value = measured;

    const heightLabel = measured === "l" ? "Length (cm):" : "Height (cm):";
    const weightLenheiLabel = measured === "l" ? "Weight for Length:" : "Weight for Height:";
    const lenheiAgeLabel = measured === "l" ? "Length for Age:" : "Height for Age:";

    document.querySelector('label[for="height"]').textContent = heightLabel;
    document.querySelector("#weight_lenhei_result .result-title").textContent = weightLenheiLabel;
    document.querySelector("#lenhei_age_result .result-title").textContent = lenheiAgeLabel;

    document.getElementById("recumbent-btn").classList.toggle("active", measured === "l");
    document.getElementById("standing-btn").classList.toggle("active", measured === "h");
}

function autoSubmit() {
    if (data && Object.keys(data).length > 0) {
        const form = document.getElementById("zscore-form");
        form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
    }
}

function calculateAgeInDays(dob, currentDay) {
    const [dobDay, dobMonth, dobYear] = dob.split("/").map(Number);
    const [currentDayDay, currentDayMonth, currentDayYear] = currentDay
        .split("/")
        .map(Number);

    // Tạo đối tượng Date từ các giá trị đã phân tích
    const birthDate = new Date(dobYear, dobMonth - 1, dobDay);
    const currentDate = new Date(
        currentDayYear,
        currentDayMonth - 1,
        currentDayDay,
    );

    // Tính tuổi bằng ngày
    const timeDifference = currentDate - birthDate;
    const ageInDays = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

    return ageInDays;
}

// Hàm kiểm tra và cập nhật trạng thái nút đo
function updateMeasuredButtons(totalMonths) {
        const isAbove5Years = totalMonths > 60; 
        const recumbentBtn = document.getElementById("recumbent-btn");
        const standingBtn = document.getElementById("standing-btn");

        if (isAbove5Years) {
                // Vô hiệu hóa Recumbent và mặc định chọn Standing
                recumbentBtn.disabled = true;
                standingBtn.disabled = true;
                selectMeasured("h");
                standingBtn.classList.add("active");
                recumbentBtn.classList.remove("active");
        } else {
                // Kích hoạt lại các nút nếu trẻ dưới 5 tuổi
                recumbentBtn.disabled = false;
                standingBtn.disabled = false;

                // Tự động chọn đo Standing nếu tháng >= 24, ngược lại chọn Recumbent
                if (totalMonths >= 24) {
                        selectMeasured("h");
                } else {
                        selectMeasured("l");
                }
        }
}

function initializeMeasured() {
    const measured = document.getElementById("measured").value; // Lấy giá trị mặc định
    if (measured === "l") {
        document.querySelector('label[for="height"]').textContent = "Length (cm):";
        document.querySelector("#weight_lenhei_result .result-title").textContent = "Weight for Length";
        document.querySelector("#lenhei_age_result .result-title").textContent = "Length for Age:";
    } else if (measured === "h") {
        document.querySelector('label[for="height"]').textContent = "Height (cm):";
        document.querySelector("#weight_lenhei_result .result-title").textContent = "Weight for Height";
        document.querySelector("#lenhei_age_result .result-title").textContent = "Height for Age:";
    }
}

// Hàm tính tổng tháng từ tuổi nhập vào
function calculateTotalMonths(ageYears, ageMonths) {
    return ageYears * 12 + ageMonths;
}

function updateAgeDisplay() {
    const ageOption = document.getElementById("age-option").value;
    const ageDisplayElement = document.getElementById("age-display");
    const form = document.getElementById("zscore-form");
    const dobInput = document.getElementById("dob"); 
    
    if (ageOption === "dob") {
        const dob = document.getElementById("dob").value;
        const currentDay = document.getElementById("current-day").value;

        if (dob && currentDay) {
            const [dobDay, dobMonth, dobYear] = dob.split("/").map(Number);
            const birthDate = new Date(dobYear, dobMonth - 1, dobDay);

            const [currentDayDay, currentDayMonth, currentDayYear] = currentDay.split("/").map(Number);
            const currentDate = new Date(currentDayYear, currentDayMonth - 1, currentDayDay);

            let ageYears = currentDate.getFullYear() - birthDate.getFullYear();
            let ageMonths = currentDate.getMonth() - birthDate.getMonth();
            let ageDays = currentDate.getDate() - birthDate.getDate();

            if (ageMonths < 0 || (ageMonths === 0 && ageDays < 0)) {
                ageYears--;
                ageMonths += 12;
            }
            if (ageDays < 0) {
                const prevMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 0);
                ageDays += prevMonth.getDate();
                ageMonths--;
            }

            const totalMonths = calculateTotalMonths(ageYears, ageMonths);

            // Kiểm tra nếu tuổi vượt quá 228 tháng
            if (totalMonths > 228) {
                showAlert("Age exceeds 228 months (19 years). Submission is not allowed.");
                dobInput.value = "";
                ageDisplayElement.innerHTML = "";
                if (form) {
                    form.addEventListener("submit", function (event) {
                        event.preventDefault(); // Ngăn form submit
                    });
                }
                return;
            }

            // Gọi hàm kiểm tra trạng thái nút đo
            updateMeasuredButtons(totalMonths);

            let ageDisplayText = "";
            if (ageYears === 0 && ageMonths === 0 && ageDays <= 30) {
                ageDisplayText = `<b>Age:</b> ${ageDays} day(s)`;
            } else if (ageYears === 0 && ageMonths <= 12) {
                ageDisplayText = `<b>Age:</b> ${ageMonths}mo ${ageDays}d`;
            } else {
                ageDisplayText = `<b>Age:</b> ${ageYears}yr ${ageMonths}mo ${ageDays}d`;
            }

            ageDisplayElement.innerHTML = ageDisplayText;
        }
    } else if (ageOption === "months") {
        const months = parseInt(document.getElementById("age-months").value, 10);
        if (!isNaN(months)) {
            if (months > 228) {
                showAlert("Age exceeds 228 months (19 years). Submission is not allowed.");
                dobInput.value = "";
                ageDisplayElement.innerHTML = "";
                if (form) {
                    form.addEventListener("submit", function (event) {
                        event.preventDefault(); // Ngăn form submit
                    });
                }
                return;
            }

            if (months >= 12) {
                const years = Math.floor(months / 12);
                const remainingMonths = months % 12;
                ageDisplayElement.innerHTML = `<b>Age:</b> ${years}yr ${remainingMonths}mo`;
            } else {
                ageDisplayElement.innerHTML = `<b>Age:</b> ${months}mo`;
            }

            // Gọi hàm kiểm tra trạng thái nút đo
            updateMeasuredButtons(months);
        } else {
            ageDisplayElement.innerHTML = ""; // Xóa nội dung nếu không có giá trị
        }
    }
}

// Hàm cập nhật tất cả biểu đồ dựa trên kích thước container
function resizeCharts() {
    const chartMappings = [
        { id: "bmi-chart" },
        { id: "wfa-chart" },
        { id: "lhfa-chart" },
        { id: "wflh-chart" },
    ];

    // Tỷ lệ cố định: Chiều rộng : Chiều cao (4:3)
    const aspectRatio = 4 / 3;

    chartMappings.forEach((chart) => {
        const chartContainer = document.getElementById(chart.id);

        if (chartContainer && chartContainer.data) {
            try {
                const chartWidth = chartContainer.offsetWidth;
                const chartHeight = chartWidth / aspectRatio;

                // Cập nhật layout với chiều cao mới và font chữ động
                const newLayout = {
                    ...chartContainer.layout,
                    height: chartHeight, // Tính chiều cao dựa trên tỷ lệ
                    font: {
                        ...chartContainer.layout.font,
                        size: Math.max(8, chartWidth * 0.02),
                    },
                };

                Plotly.react(chart.id, chartContainer.data, newLayout);
            } catch (error) {
                console.error(`Lỗi khi resize biểu đồ ${chart.id}:`, error);
            }
        }
    });
}

// Hàm cập nhật biểu đồ dựa trên loại được chọn
function updateChartsBasedOnSelection() {
    const selectedType = document.getElementById("chart-type-selector").value;

    const chartMappings = [
        { key: "bmi", id: "bmi-chart" },
        { key: "wfa", id: "wfa-chart" },
        { key: "lhfa", id: "lhfa-chart" },
        { key: "wflh", id: "wflh-chart" },
    ];

    const aspectRatio = 4 / 3;

    chartMappings.forEach((chart) => {
        const chartContainer = document.getElementById(chart.id);

        if (data.charts[chart.key] && chartContainer) {
            const chartData = data.charts[chart.key][selectedType];
            if (chartData && chartData.data) {
                try {
                    Plotly.purge(chart.id);

                    const parsedData = JSON.parse(chartData.data);

                    const chartWidth = chartContainer.offsetWidth;
                    const chartHeight = chartWidth / aspectRatio;

                    // Gán dữ liệu vào container để dùng khi resize
                    chartContainer.data = parsedData.data;
                    chartContainer.layout = {
                        ...parsedData.layout,
                        autosize: true,
                        height: chartHeight,
                        margin: { l: 10, r: 10, t: 10, b: 10 },
                        font: {
                            ...parsedData.layout.font,
                            size: Math.max(8, chartWidth * 0.02),
                        },
                    };

                    const config = { ...chartData.config, responsive: true };

                    Plotly.newPlot(chart.id, chartContainer.data, chartContainer.layout, config);
                } catch (error) {
                    console.error(`Lỗi khi cập nhật biểu đồ ${chart.key}:`, error);
                }
            }
        }
    });
}

function updateResults(data) {
    const noDataMessage = document.getElementById('no-data-message');
    const collapsibleContent = document.getElementById('collapsible-content');
    
    if (!data || Object.keys(data).length === 0) {
        // Hiển thị thông báo "No data"
        noDataMessage.style.visibility = 'visible';
        noDataMessage.style.height = 'auto';

        // Ẩn các kết quả cũ
        collapsibleContent.style.visibility = 'hidden';
        collapsibleContent.style.height = '-200px'; 
        if (collapsibleContent.classList.contains('expand')) {
            toggleCollapse('collapsible-content', 'arrow-icon');
        }
    } else {
        // Nếu có dữ liệu, ẩn thông báo "No data"
        noDataMessage.style.visibility = 'hidden';
        noDataMessage.style.height = '0px';

        // Hiển thị các kết quả
        collapsibleContent.style.visibility = 'visible';
        collapsibleContent.style.height = 'auto';
        // Hiển thị nội dung và tự động mở rộng nếu chưa mở
        if (!collapsibleContent.classList.contains('expand')) {
            toggleCollapse('collapsible-content', 'arrow-icon');
        }
        resizeCharts(); // Gọi resize ngay lập tức
    }
}


function calculateIBW() {
    const height = parseFloat(document.getElementById("height").value);
    const actualWeight = parseFloat(
        document.getElementById("actualWeight").value,
    );

    // Kiểm tra các điều kiện nhập vào
    if (!gender || isNaN(height) || height < 152 || height > 250) {
        document.getElementById("resultIBW").style.display = "none";
        document.getElementById("text1").style.display = "block"; // Hiển thị placeholder
        document.getElementById("warningMessage").textContent =
            "Warning: You entered a height of less than 5 ft (1.52m).";
        return;
    } else {
        document.getElementById("warningMessage").textContent = "";
    }

    // Tính IBW dựa trên giới tính và chiều cao
    let ibw;
    if (gender === "male") {
        ibw = 50 + 2.3 * (height / 2.54 - 60); // Chuyển chiều cao từ cm sang inches
    } else {
        ibw = 45.5 + 2.3 * (height / 2.54 - 60);
    }
    ibw = ibw.toFixed(2);

    const ibwOutput = document.getElementById("ibw-output");
    const abwOutput = document.getElementById("abw-output");
    const ibwItem = ibwOutput.parentElement;
    const abwItem = abwOutput.parentElement;

    ibwOutput.innerHTML = `${ibw} kg`; // Hiển thị IBW

    // Kiểm tra xem người dùng có nhập Actual Weight không, nếu có thì tính và hiển thị ABW
    if (!isNaN(actualWeight) && actualWeight > 0) {
        if (actualWeight > ibw) {
            // Tính ABW nếu Actual Weight lớn hơn IBW
            const abw = (parseFloat(ibw) + 0.4 * (actualWeight - ibw)).toFixed(
                2,
            );
            abwOutput.innerHTML = `${abw} kg`;
            abwItem.querySelector("span").innerHTML = "Adjusted Body Weight"; // Khôi phục nhãn ABW bình thường
            ibwItem.classList.add("with-border"); // Thêm border khi hiển thị cả ABW và IBW
        } else {
            // Hiển thị thông báo nếu Actual Weight nhỏ hơn hoặc bằng IBW
            abwOutput.innerHTML = "";
            abwItem.querySelector("span").innerHTML =
                "Adjusted body weight only applicable if actual body weight is greater than ideal body weight";
            ibwItem.classList.add("with-border"); // Thêm border khi hiển thị thông báo
        }
        abwItem.style.display = "flex"; // Hiển thị ô ABW nếu có giá trị hoặc thông báo
    } else {
        abwItem.style.display = "none"; // Ẩn ABW nếu không có giá trị
        ibwItem.classList.remove("with-border"); // Xóa border khi chỉ có IBW
    }

    document.getElementById("text1").style.display = "none"; // Ẩn placeholder
    document.getElementById("resultIBW").style.display = "flex"; // Hiển thị kết quả
}
