function createCard(cardId, tabContent) {
    const card = document.createElement('div');
    card.className = 'w-full flex flex-col';

    const ul = document.createElement('ul');
    ul.className = 'flex flex-row flex-wrap text-sm font-medium text-center text-gray-500';
    ul.id = cardId + 'Tab';
    ul.setAttribute('role', 'tablist');

    const contentDiv = document.createElement('div');
    contentDiv.id = cardId + 'TabContent';

    tabContent.forEach((tab, index) => {
        const li = document.createElement('li');
        li.className = 'mr-2 mb-2';

        const button = document.createElement('button');
        button.id = cardId + '-tab-' + index;
        button.setAttribute('data-tabs-target', '#' + cardId + '-content-' + index);
        button.type = 'button';
        button.role = 'tab';
        button.className = 'inline-block p-2.5 text-sm font-medium text-gray-900 rounded-lg hover:bg-opacity-0 transition-all ease-in duration-75 hover:bg-gradient-to-br from-pink-500 to-orange-400';
        button.innerText = tab.title;

        button.addEventListener('click', function() {
            document.querySelectorAll('[id^="' + cardId + '-content-"]').forEach(div => {
                div.classList.add('hidden');
            });
            const targetContentDiv = document.querySelector(this.getAttribute('data-tabs-target'));
            if (targetContentDiv) {
                targetContentDiv.classList.remove('hidden');
            }
        });

        li.appendChild(button);
        ul.appendChild(li);
    });

    card.appendChild(ul);
    card.appendChild(contentDiv);

    tabContent.forEach((tab, index) => {
        const div = document.createElement('div');
        div.id = cardId + '-content-' + index;
        div.className = 'hidden p-4 md:p-8';
        if (index === 0) {
            div.classList.remove('hidden');
        }
        div.innerHTML = typeof tab.content === 'function' ? tab.content() : tab.content;
        contentDiv.appendChild(div);
    });

    return card;
}

