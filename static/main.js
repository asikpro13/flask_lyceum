let id_job = null
let edit_id = null

function delete_job() {
    fetch('/del_job/' + id_job)  // Удаление записи работы
}

function last_id(last_id) {
    id_job = last_id
}

function last_id_python(last_id) {
     edit_id = last_id
    fetch('/last_user/' + last_id).then(function (response) {
        return response.json()
    })
        .then(function (data) {
            document.getElementById('editTitle').value = data.title_of_activity
            document.getElementById('editTeamLeader').value = data.team_leader
            document.getElementById('editDuration').value = data.duration
            document.getElementById('editListOfCollaborators').value = data.collaborators
            if (data.finished === true) {
                document.getElementById('finish').checked = true
            }
            else if (data.finished === false){
                document.getElementById('finish').checked = false
            }
        })  // Редактирование записи работы

}

function edit_job() {
    fetch('/edit_job', {
        method: 'POST',
        body: JSON.stringify({
            'id_job': edit_id,
            'title': document.getElementById('editTitle').value,
            'teamLeader': document.getElementById('editTeamLeader').value,
            'duration': document.getElementById('editDuration').value,
            'collaborators': document.getElementById('editListOfCollaborators').value,
            'is_finished': document.getElementById('finish').checked
        })
    })
    window.location.reload()

}