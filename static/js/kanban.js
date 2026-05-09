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

    function updateColumnState(column) {
        const cardsInColumn = column.querySelectorAll('[data-job-card]');
        const emptyState = column.querySelector('[data-empty-state]');
        const emptyMessage = column.dataset.emptyMessage || 'No jobs found.';
        const countBadge = column.previousElementSibling?.querySelector('[data-job-count]');

        if (countBadge) {
            countBadge.textContent = cardsInColumn.length.toString();
        }

        if (cardsInColumn.length === 0) {
            if (!emptyState) {
                const placeholder = document.createElement('div');
                placeholder.dataset.emptyState = 'true';
                placeholder.className = 'rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-sm text-slate-500';
                placeholder.textContent = emptyMessage;
                column.appendChild(placeholder);
            }
            return;
        }

        if (emptyState) {
            emptyState.remove();
        }
    }

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
                const targetColumn = document.querySelector(`[data-job-column][data-status="${targetStatus}"]`);
                if (targetColumn && card) {
                    const oldParent = card.parentElement;
                    card.classList.remove('opacity-60');
                    targetColumn.appendChild(card);

                    card.style.transition = 'transform 0.18s ease, box-shadow 0.18s ease';
                    card.style.transform = 'scale(1.02)';
                    card.style.boxShadow = '0 8px 30px rgba(2,6,23,0.1)';
                    setTimeout(() => {
                        card.style.transform = '';
                        card.style.boxShadow = '';
                    }, 300);

                    if (oldParent) updateColumnState(oldParent);
                    updateColumnState(targetColumn);
                } else {
                    window.location.reload();
                }
            } else {
                let message = 'Unable to move job due to appointment time and status constraints.';
                try {
                    const payload = await response.json();
                    if (payload && payload.error) {
                        message = payload.error;
                    }
                } catch (_err) {
                    // Keep default message when response is not JSON.
                }
                alert(message);
            }
        });
    });

    columns.forEach(updateColumnState);
}

document.addEventListener('DOMContentLoaded', initKanban);
