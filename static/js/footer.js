document.addEventListener("DOMContentLoaded", function () {
    
    const footer = document.createElement('footer');

    Object.assign(footer.style, {
        backgroundColor: '#f18e3c', 
        color: 'white', 
        textAlign: 'center',
        padding: '20px 0',
        marginTop: 'auto', 
        width: '100%',
        position: 'relative',
        bottom: '0',
        left: '0',
        fontSize: '1rem'
    });

    const address = document.createElement('p');
    address.textContent = 'Address: G H Raisoni College of Engineering, CRPF Gate, No.3, Hingna Rd, Digdoh Hills, Nagpur, Maharashtra 440016';
    const contact = document.createElement('p');
    contact.textContent = 'Contact: email@example.com | 099210 08657';
    const openingTime = document.createElement('p');
    openingTime.textContent = 'Opening Hours: Monday - Friday, 9:00 AM to 5:00 PM';

    footer.appendChild(address);
    footer.appendChild(contact);
    footer.appendChild(openingTime);

    document.body.appendChild(footer);

    document.body.style.display = 'flex';
    document.body.style.flexDirection = 'column';
    document.body.style.minHeight = '100vh';
});