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
