let sidebarOpen = false;
let gender = '';

function toggleSidebar() {
    const sidebar = document.getElementById("mySidebar");
    const tooltip = document.querySelector(".tooltip-text");
    const iconContainer = document.querySelector(".icon-container");
    const overlay = document.getElementById("myOverlay");

    if (sidebarOpen) {
        tooltip.textContent = "Mở Sidebar";
        document.body.classList.remove('sidebar-open');
        sidebarOpen = false;
    } else {
        tooltip.textContent = "Đóng Sidebar";
        tooltip.style.visibility = "hidden";
        document.body.classList.add('sidebar-open');
        sidebarOpen = true;
    }

    // Hiển thị/ẩn overlay
    overlay.style.display = sidebarOpen ? 'block' : 'none';

    // Khi hover lại icon, tooltip sẽ hiện lại
    iconContainer.onmouseover = function() {
        tooltip.style.visibility = "visible";
    };
}
function validateFiO2() {
    const fio2Input = document.getElementById('fio2').value;
    const totalFlowInput = document.getElementById('totalFlow').value;

    // Kiểm tra FiO2 có hợp lệ hay không
    if (fio2Input < 21 || fio2Input > 100) {
      alert('FiO2 phải nằm trong khoảng từ 21 đến 100%. Vui lòng nhập lại.');
      document.getElementById('airFlow').value = '';
      document.getElementById('oxyFlow').value = '';
      return false; // Ngăn không cho form submit hoặc tính toán
    }
    calculateFlow();
    return false;
}
    function calculateFlow() {
        const fio2 = parseFloat(document.getElementById('fio2').value);
        const totalFlow = parseFloat(document.getElementById('totalFlow').value);
    
        // Hiển thị cảnh báo nếu FiO2 > 80%
        const warningMessage = document.getElementById('warningMessage');
        if (fio2 > 80) {
            warningMessage.textContent = "Warning: FiO2 value should not exceed 80%!";
        } else {
            warningMessage.textContent = "";
        }
    
        if (isNaN(fio2) || isNaN(totalFlow)) {
            alert("Please enter valid FiO2 and Total Flow values.");
            return;
        }            
    
        // Công thức tính Air Flow và Oxy Flow
        const airFlow = totalFlow - ((fio2 * totalFlow - 21 * totalFlow) / 79);
        const oxyFlow = totalFlow - airFlow;
    
        // Hiển thị kết quả
        document.getElementById('airFlow').textContent = "Air Flow: " + airFlow.toFixed(2) + " L/min";
        document.getElementById('oxyFlow').textContent = "Oxy Flow: " + oxyFlow.toFixed(2) + " L/min";
    }


function loadPage(page) {
    // Load nội dung trang và lưu vào sessionStorage
    fetch(`/${page}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('main').innerHTML = html;
            sessionStorage.setItem('lastPage', page); // Lưu trang hiện tại
        });
}

// Xóa sessionStorage khi chọn trang chủ
function clearLastPage() {
    sessionStorage.removeItem('lastPage');
}

// Kiểm tra và tải lại trang cuối cùng khi load lại trang
window.addEventListener('load', function() {
    const lastPage = sessionStorage.getItem('lastPage');
    if (lastPage) {
        loadPage(lastPage);
    }
});


function highlightSelected(selectedId) {
    // Xóa lớp "selected" từ các mục khác
    var items = document.querySelectorAll('.sidebar a');
    items.forEach(function(item) {
        item.classList.remove('selected');
    });

    // Thêm lớp "selected" cho mục đang được chọn
    var selectedItem = document.getElementById(selectedId);
    selectedItem.classList.add('selected');

    // Lưu lại mục được chọn vào localStorage
    sessionStorage.setItem('selectedItem', selectedId);
}

function calculateETT() {
    const age = parseInt(document.getElementById('ageInput').value);

    // Kiểm tra giá trị của tuổi trong khoảng từ 1 đến 12
    if (age < 1 || age > 12 || isNaN(age)) {
        alert("Vui lòng nhập tuổi hợp lệ từ 1 đến 12.");
        return;
    }

    // Tính toán NKQ không bóng và có bóng
    const ettWithoutCuff = (age / 4) + 4;
    const ettWithCuff = (age / 4) + 3.5;

    // Tính toán độ sâu nội khí quản
    const ettDepth = ettWithCuff * 3; // Công thức tính độ sâu: ETT với bóng * 3
    document.getElementById('age').textContent = age;
    // Hiển thị kết quả
    document.getElementById('ettWithoutCuff').textContent = ettWithoutCuff.toFixed(1) + " mm";
    document.getElementById('ettWithCuff').textContent = ettWithCuff.toFixed(1) + " mm";
    document.getElementById('ettDepth').textContent = ettDepth.toFixed(1) + " cm";

    // Ẩn form nhập liệu và hiện kết quả
    document.getElementById('formBox').style.display = 'none';
    document.getElementById('resultBoxes').style.display = 'block';
    document.getElementById('resetBtn').style.display = 'inline-block';
}

function resetForm() {
    // Ẩn kết quả và hiển thị lại form nhập liệu
    document.getElementById('resultBoxes').style.display = 'none';
    document.getElementById('resetBtn').style.display = 'none';
    document.getElementById('formBox').style.display = 'block';

    // Reset giá trị của form
    document.getElementById('ageInput').value = '';
}

function calculateBMIandBSA() {
    var weight = document.getElementById('weight').value;
    var height = document.getElementById('height').value;
        // Kiểm tra xem các trường có để trống hay không
        if (!weight || !height) {
            warningMessage.textContent = "Warning: Please enter both weight and height.";
            // Ẩn kết quả nếu chưa nhập đủ dữ liệu
            document.getElementById('resultBoxBMI').style.display = 'none';
            document.getElementById('text1').style.display = 'block'; // Hiển thị placeholder
            return;
        } else {
            warningMessage.textContent = "";
        }
    if (weight && height) {
        // Tính BMI
        var heightInMeters = height / 100; // Chuyển đổi chiều cao từ cm sang mét
        var bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1); // Tính BMI và làm tròn

        var bmiCategory = '';
        if (bmi < 18.5) {
            bmiCategory = 'Underweight';
        } else if (bmi >= 18.5 && bmi <= 24.9) {
            bmiCategory = 'Normal weight';
        } else if (bmi >= 25 && bmi <= 29.9) {
            bmiCategory = 'Overweight';
        } else if (bmi >= 30 && bmi <= 34.9) {
            bmiCategory = 'Obese (Class 1)';
        } else if (bmi >= 35 && bmi <= 39.9) {
            bmiCategory = 'Obese (Class 2)';
        } else {
            bmiCategory = 'Obese (Class 3)';
        }

        document.getElementById('bmi-output').innerHTML = `${bmi} kg/m²`;
        document.getElementById('bmiCategory-output').innerHTML = `${bmiCategory}`;
        // Tính BSA sử dụng công thức Mosteller
        var bsa = Math.sqrt((weight * height) / 3600).toFixed(2); // Tính BSA và làm tròn
        document.getElementById('bsa-output').innerHTML = `${bsa} m²`;
    } else {
        document.getElementById('bmi-output').innerHTML = 'Please fill out required fields.';
        document.getElementById('bsa-output').innerHTML = '';
    }

        document.getElementById('text1').style.display = 'none'; // Ẩn placeholder
        document.getElementById('resultBoxBMI').style.display = 'flex';   // Hiển thị kết quả
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
    document.getElementById('serumProtein').dataset.unit = "g/dL";
    document.getElementById('pleuralFluidProtein').dataset.unit = "g/dL";

function calculateLightCriteria() {
    const serumProteinInput = document.getElementById('serumProtein');
    const pleuralFluidProteinInput = document.getElementById('pleuralFluidProtein');
    const serumLDH = parseFloat(document.getElementById('serumLDH').value);
    const pleuralFluidLDH = parseFloat(document.getElementById('pleuralFluidLDH').value);
    const upperLimitLDH = parseFloat(document.getElementById('upperLimitLDH').value);

    let serumProtein = parseFloat(serumProteinInput.value);
    let pleuralFluidProtein = parseFloat(pleuralFluidProteinInput.value);

    // Check if serum and pleural fluid proteins are in the same unit
    if (serumProteinInput.dataset.unit !== pleuralFluidProteinInput.dataset.unit) {
        // Convert pleural fluid protein to match serum protein unit
        if (serumProteinInput.dataset.unit === "g/dL" && pleuralFluidProteinInput.dataset.unit === "g/L") {
            pleuralFluidProtein /= 10; // Convert from g/L to g/dL
        } else if (serumProteinInput.dataset.unit === "g/L" && pleuralFluidProteinInput.dataset.unit === "g/dL") {
            pleuralFluidProtein *= 10; // Convert from g/dL to g/L
        }
    }

    if (isNaN(serumProtein) || isNaN(pleuralFluidProtein) || isNaN(serumLDH) || isNaN(pleuralFluidLDH) || isNaN(upperLimitLDH)) {
        document.getElementById('warningMessage').textContent = "Warning: Please enter all values.";
        return;
    } else {
            warningMessage.textContent = "";
        }

    const criteria1 = pleuralFluidProtein / serumProtein > 0.5;
    const criteria2 = pleuralFluidLDH / serumLDH > 0.6;
    const criteria3 = pleuralFluidLDH > (2 / 3) * upperLimitLDH;

    const criteriaMet = [criteria1, criteria2, criteria3].filter(Boolean).length;
    const result = (criteria1 || criteria2 || criteria3) ? "Exudative Effusion" : "Transudative Effusion";
    document.getElementById('resultLight').innerHTML = `${result} (Criteria Met: ${criteriaMet}/3)`;
    document.getElementById('text1').style.display = 'none';
    document.getElementById('resultBoxLight').style.display = 'flex';
}

        function selectGender(selectedGender) {
            gender = selectedGender;
            document.getElementById('male-btn').classList.remove('active');
            document.getElementById('female-btn').classList.remove('active');
            if (selectedGender === 'male') {
                document.getElementById('male-btn').classList.add('active');
            } else {
                document.getElementById('female-btn').classList.add('active');
            }
        }

    function calculateIBW() {
        const height = parseFloat(document.getElementById('height').value);
        const actualWeight = parseFloat(document.getElementById('actualWeight').value);
    
        // Kiểm tra các điều kiện nhập vào
        if (!gender || isNaN(height) || height < 152 || height > 250) {
            document.getElementById('resultIBW').style.display = 'none';
            document.getElementById('text1').style.display = 'block'; // Hiển thị placeholder               
            document.getElementById('warningMessage').textContent = "Warning: You entered a height of less than 5 ft (1.52m).";
            return;
        } else {
            document.getElementById('warningMessage').textContent = "";
        }
    
        // Tính IBW dựa trên giới tính và chiều cao
        let ibw;
        if (gender === 'male') {
            ibw = 50 + 2.3 * ((height / 2.54) - 60); // Chuyển chiều cao từ cm sang inches
        } else {
            ibw = 45.5 + 2.3 * ((height / 2.54) - 60);
        }
        ibw = ibw.toFixed(2);
        
        const ibwOutput = document.getElementById('ibw-output');
        const abwOutput = document.getElementById('abw-output');
        const ibwItem = ibwOutput.parentElement;
        const abwItem = abwOutput.parentElement;
    
        ibwOutput.innerHTML = `${ibw} kg`; // Hiển thị IBW
    
        // Kiểm tra xem người dùng có nhập Actual Weight không, nếu có thì tính và hiển thị ABW
        if (!isNaN(actualWeight) && actualWeight > 0) {
            if (actualWeight > ibw) {
                // Tính ABW nếu Actual Weight lớn hơn IBW
                const abw = (parseFloat(ibw) + 0.4 * (actualWeight - ibw)).toFixed(2);
                abwOutput.innerHTML = `${abw} kg`;
                abwItem.querySelector("span").innerHTML = "Adjusted Body Weight"; // Khôi phục nhãn ABW bình thường
                ibwItem.classList.add('with-border'); // Thêm border khi hiển thị cả ABW và IBW
            } else {
                // Hiển thị thông báo nếu Actual Weight nhỏ hơn hoặc bằng IBW
                abwOutput.innerHTML = "";
                abwItem.querySelector("span").innerHTML = "Adjusted body weight only applicable if actual body weight is greater than ideal body weight";
                ibwItem.classList.add('with-border'); // Thêm border khi hiển thị thông báo
            }
            abwItem.style.display = 'flex'; // Hiển thị ô ABW nếu có giá trị hoặc thông báo
        } else {
            abwItem.style.display = 'none'; // Ẩn ABW nếu không có giá trị
            ibwItem.classList.remove('with-border'); // Xóa border khi chỉ có IBW
        }

        document.getElementById('text1').style.display = 'none'; // Ẩn placeholder
        document.getElementById('resultIBW').style.display = 'flex'; // Hiển thị kết quả
    }

