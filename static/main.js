let id_job = null

function delete_job() {
    fetch('/del_user/' + id_job)  // Удаление записи работы
}

function last_id(last_id) {
    id_job = last_id
    console.log(id_job)
}