function createFormInput(id, label, value, type = 'text', additionalClasses = '') {
    const inputType = type === 'checkbox' ? `<input type="checkbox" class="form-check-input ${additionalClasses}" id="${id}" ${value ? 'checked' : ''}>` : `<input type="text" class="form-control ${additionalClasses}" id="${id}" value="${value}">`;

    return `
        <div class="${type === 'checkbox' ? 'col-md-4 form-check' : 'col-md-4'}">
            <label for="${id}" class="form-label">${label}</label>
            ${inputType}
        </div>
    `;
}
function createSection(id, title, inputs, data) {
    return `
        <h5>
            <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#${id}${data.id}" aria-expanded="true" aria-controls="${id}${data.id}">
                ${title}
            </button>
        </h5>
        <div id="${id}${data.id}" class="collapse" aria-labelledby="heading${data.id}">
            <div class="row card-content">
                ${inputs.map(input => createFormInput(`${input.id}${data.id}`, input.label, input.value, input.type, input.additionalClasses)).join('')}
            </div>
        </div>
    `;
}

export { createSection  }
