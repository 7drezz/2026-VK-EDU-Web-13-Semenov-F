function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function sendVote(url, value, callback) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: 'value=' + value,
        redirect: 'manual'
    })
    .then(response => {
        if (response.status === 403 || response.status === 401 || response.status === 302 || response.status === 0) {
            const currentUrl = encodeURIComponent(window.location.href);
            window.location.href = `/login/?next=${currentUrl}`;
            return null;
        }
        if (!response.ok) {
            return response.json().then(data => {
                alert(data.error || 'Something went wrong');
                return null;
            });
        }
        return response.json();
    })
    .then(data => {
        if (data && callback) {
            callback(data);
        }
    })
    .catch(error => {
        console.error(error);
        const currentUrl = encodeURIComponent(window.location.href);
        window.location.href = `/login/?next=${currentUrl}`;
    });
}

function markAnswer(answerId) {
    if (!confirm('Mark this answer as correct?')) return;
    
    const url = `/api/answer/${answerId}/correct/`;
    
    fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.success) {
            location.reload();
        }
    })
    .catch(error => console.error(error));
}

function unmarkAnswer(answerId) {
    if (!confirm('Unmark this answer as correct?')) return;
    
    const url = `/api/answer/${answerId}/unmark/`;
    
    fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.success) {
            location.reload();
        }
    })
    .catch(error => console.error(error));
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.question-like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const questionId = this.dataset.questionId;
            const value = parseInt(this.dataset.value);
            const url = `/api/question/${questionId}/like/`;
            const ratingSpan = document.querySelector(`.question-rating-${questionId}`);
            
            sendVote(url, value, function(data) {
                if (ratingSpan) ratingSpan.textContent = data.rating;
                const upBtn = document.querySelector(`.question-up-${questionId}`);
                const downBtn = document.querySelector(`.question-down-${questionId}`);
                if (upBtn && downBtn) {
                    if (data.user_vote === 1) {
                        upBtn.classList.add('btn-success');
                        upBtn.classList.remove('btn-outline-success');
                        downBtn.classList.remove('btn-danger');
                        downBtn.classList.add('btn-outline-danger');
                    } else if (data.user_vote === -1) {
                        downBtn.classList.add('btn-danger');
                        downBtn.classList.remove('btn-outline-danger');
                        upBtn.classList.remove('btn-success');
                        upBtn.classList.add('btn-outline-success');
                    } else {
                        upBtn.classList.remove('btn-success');
                        upBtn.classList.add('btn-outline-success');
                        downBtn.classList.remove('btn-danger');
                        downBtn.classList.add('btn-outline-danger');
                    }
                }
            });
        });
    });
    
    document.querySelectorAll('.answer-like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const answerId = this.dataset.answerId;
            const value = parseInt(this.dataset.value);
            const url = `/api/answer/${answerId}/like/`;
            const ratingSpan = document.querySelector(`.answer-rating-${answerId}`);
            
            sendVote(url, value, function(data) {
                if (ratingSpan) ratingSpan.textContent = data.rating;
                const upBtn = document.querySelector(`.answer-up-${answerId}`);
                const downBtn = document.querySelector(`.answer-down-${answerId}`);
                if (upBtn && downBtn) {
                    if (data.user_vote === 1) {
                        upBtn.classList.add('btn-success');
                        upBtn.classList.remove('btn-outline-success');
                        downBtn.classList.remove('btn-danger');
                        downBtn.classList.add('btn-outline-danger');
                    } else if (data.user_vote === -1) {
                        downBtn.classList.add('btn-danger');
                        downBtn.classList.remove('btn-outline-danger');
                        upBtn.classList.remove('btn-success');
                        upBtn.classList.add('btn-outline-success');
                    } else {
                        upBtn.classList.remove('btn-success');
                        upBtn.classList.add('btn-outline-success');
                        downBtn.classList.remove('btn-danger');
                        downBtn.classList.add('btn-outline-danger');
                    }
                }
            });
        });
    });
    
    document.querySelectorAll('.mark-correct-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const answerId = this.dataset.answerId;
            markAnswer(answerId);
        });
    });
    
    document.querySelectorAll('.unmark-correct-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const answerId = this.dataset.answerId;
            unmarkAnswer(answerId);
        });
    });
});