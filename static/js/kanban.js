function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : '';
}

function initKanban() {
    const cards = document.querySelectorAll('[data-job-card]');
    const columns = document.querySelectorAll('[data-job-column]');
    if (!cards.length || !columns.length) return;

    let draggedCardId = null;

    cards.forEach(card => {
        card.addEventListener('dragstart', () => {
            draggedCardId = card.dataset.jobId;
            card.classList.add('opacity-60');
        });
        card.addEventListener('dragend', () => card.classList.remove('opacity-60'));
    });

    columns.forEach(column => {
        column.addEventListener('dragover', event => event.preventDefault());
        column.addEventListener('drop', async event => {
            event.preventDefault();
            const targetStatus = column.dataset.status;
            if (!draggedCardId || !targetStatus) return;

            const card = document.querySelector(`[data-job-id="${draggedCardId}"]`);
            if (!card) return;

            const response = await fetch(card.dataset.updateUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ status: targetStatus }),
            });

            if (response.ok) {
                // Optimistic UI: move card to target column without reload
                const targetColumn = document.querySelector(`[data-job-column][data-status="${targetStatus}"]`);
                if (targetColumn && card) {
                    // remove from old parent and append to new column
                    card.classList.remove('opacity-60');
                    const oldParent = card.parentElement;
                    targetColumn.appendChild(card);

                    // tiny visual feedback
                    card.style.transition = 'transform 0.18s ease, box-shadow 0.18s ease';
                    card.style.transform = 'scale(1.02)';
                    card.style.boxShadow = '0 8px 30px rgba(2,6,23,0.1)';
                    setTimeout(() => {
                        card.style.transform = '';
                        card.style.boxShadow = '';
                    }, 300);

                    // update counts badges if present
                    try {
                        const dec = oldParent.previousElementSibling?.querySelector('span');
                        const inc = targetColumn.previousElementSibling?.querySelector('span');
                        if (dec) dec.textContent = Math.max(0, parseInt(dec.textContent || '0') - 1);
                        if (inc) inc.textContent = (parseInt(inc.textContent || '0') + 1).toString();
                    } catch (e) {
                        // ignore UI count update errors
                    }
                } else {
                    window.location.reload();
                }
            } else {
                // show a brief error if update failed
                alert('Unable to move job. Please refresh and try again.');
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', initKanban);
