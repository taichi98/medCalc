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
function validateFiO2() {
    const fio2Input = document.getElementById('fio2').value;
    if (fio2Input < 21 || fio2Input > 100) {
      alert('FiO2 phải nằm trong khoảng từ 21 đến 100%. Vui lòng nhập lại.');
      return false; // Ngăn không cho form submit hoặc tính toán
    }
    return true; // Cho phép submit hoặc tính toán nếu hợp lệ
}

function loadPage(page) {
            fetch(page)
            .then(response => response.text())
            .then(data => {
                document.getElementById('main').innerHTML = data;
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
}

function calculateETT() {
        // Lấy giá trị từ form
        let age = parseInt(document.getElementById("age").value);
        let type = document.getElementById("type").value;
    
        // Tính toán cỡ ống nội khí quản (ETT size)
        let ettSize;
        if (type === "cuffed") {
            ettSize = (age / 4) + 3.5; // Có bóng chèn
        } else {
            ettSize = (age / 4) + 4;   // Không bóng chèn
        }
    
        // Tính toán độ sâu nội khí quản
        let depth = ettSize * 3;
    
        // Hiển thị kết quả
        document.getElementById("ettSize").innerText = "ETT Size: " + ettSize.toFixed(1);
        document.getElementById("depth").innerText = "Độ sâu nội khí quản: " + depth.toFixed(1) + " cm";
    }

