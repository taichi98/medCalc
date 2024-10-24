let sidebarOpen = false;

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
    fetch(page)
        .then(response => response.text())
        .then(data => {
            document.getElementById('main').innerHTML = data;
            // Lưu lại trang hiện tại vào localStorage
            sessionStorage.setItem('lastPage', page);
        })
        .catch(error => {
            console.error('Error loading page:', error);
        });
}

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

// Hàm để tải lại trang cuối cùng khi tải lại trang web
function loadLastPage() {
    // Kiểm tra xem trang cuối cùng đã được lưu trong localStorage hay chưa
    var lastPage = sessionStorage.getItem('lastPage');
    if (lastPage) {
        loadPage(lastPage);
    } else {
        // Nếu không có, mặc định tải trang cpap.html
        loadPage('cpap.html');
    }

    // Kiểm tra xem mục được chọn cuối cùng đã được lưu trong localStorage hay chưa
    var selectedItem = sessionStorage.getItem('selectedItem');
    if (selectedItem) {
        highlightSelected(selectedItem);
    } else {
        // Nếu không có, mặc định chọn mục đầu tiên (item1)
        highlightSelected('item1');
    }
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
    document.getElementById('age').value = '';
}

function calculateBMIandBSA() {
    var weight = document.getElementById('weight').value;
    var height = document.getElementById('height').value;

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

        document.getElementById('bmi-output').innerHTML = `Your BMI is: ${bmi} (${bmiCategory})`;

        // Tính BSA sử dụng công thức Mosteller
        var bsa = Math.sqrt((weight * height) / 3600).toFixed(2); // Tính BSA và làm tròn
        document.getElementById('bsa-output').innerHTML = `Your BSA is: ${bsa} m²`;
    } else {
        document.getElementById('bmi-output').innerHTML = 'Please fill out required fields.';
        document.getElementById('bsa-output').innerHTML = '';
    }

        document.getElementById('text1').style.display = 'none'; // Ẩn placeholder
        document.getElementById('resultBoxBMI').style.display = 'flex';   // Hiển thị kết quả
}
