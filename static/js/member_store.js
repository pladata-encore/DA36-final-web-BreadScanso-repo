function searchMembers() {
    let searchQuery = document.getElementById("searchMember").value;

    // AJAX 요청
    fetch("{% url 'member_store' %}", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'search': searchQuery })
    })
    .then(response => response.json())
    .then(data => {
        // 검색 결과로 받은 데이터로 테이블을 갱신
        updateTable(data.members);
    })
    .catch(error => console.error("Error fetching search results:", error));
}

function updateTable(members) {
    let tbody = document.querySelector("tbody");
    tbody.innerHTML = ""; // 기존 테이블 내용 지우기

    if (members.length === 0) {
        tbody.innerHTML = "<tr><td colspan='14'>등록된 회원이 없습니다.</td></tr>";
    } else {
        members.forEach((member, index) => {
            let row = `
                <tr>
                    <td><input type="checkbox" class="member-checkbox" value="${member.id}"></td>
                    <th scope="row">${index + 1}</th>
                    <td>${member.name}</td>
                    <td>${member.username}</td>
                    <td>${member.phone_number}</td>
                    <td>${member.gender}</td>
                    <td>${member.age_group}</td>
                    <td>${member.email}</td>
                    <td>${member.visit_count}</td>
                    <td>${member.total_spent} 원</td>
                    <td>${member.join_date}</td>
                    <td>${member.last_visit_date}</td>
                    <td>${member.points}</td>
                    <td>
                        ${member.profile_picture ? `<img src="${member.profile_picture.url}" width="30">` : 'null'}
                    </td>
                    <td><button type="button" class="btn btn-light" onclick="toggleButton(this)">수정</button></td>
                </tr>
            `;
            tbody.insertAdjacentHTML('beforeend', row);
        });
    }
}
