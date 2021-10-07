const sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const getmodalUXContent = async () => {
    let modalUXContent = document.getElementsByClassName('modal-ux-content')[0];
    let counter = 0;
  
    while(!modalUXContent && counter < 10){
      await sleep(200);
      modalUXContent = document.getElementsByClassName('modal-ux-content')[0];
  
      counter += 1;
    }

    return modalUXContent;
}

const addClientId = async () => {
  let modalUXContent = await getmodalUXContent();

  let inputs = Array.from(modalUXContent.getElementsByTagName('input')).filter((input)=>{
      return input.id === 'client_id';
  });

  inputs.map((input)=>{
    let ev = new Event('input', { bubbles: true});
    ev.simulated = true;
    input.value = clientId;
    input.dispatchEvent(ev);
  })
}

const addClientSecret = async () => {
  let modalUXContent = await getmodalUXContent();

  let inputs = Array.from(modalUXContent.getElementsByTagName('input')).filter((input)=>{
    return input.id === 'client_secret';
  });

  inputs.map((input)=>{
    let ev = new Event('input', { bubbles: true});
    ev.simulated = true;
    input.value = clientSecret;
    input.dispatchEvent(ev);
  })
}

const setClientSecretAndClientId = async (event) => {
    addClientId()
    addClientSecret();
}

document.addEventListener("DOMContentLoaded", async () => {
  let authorizeButton = document.getElementsByClassName('authorize')[0];
  let counter = 0;

  while(!authorizeButton && counter < 10){
    await sleep(100);
    authorizeButton = document.getElementsByClassName('authorize')[0];

    counter += 1;
  }

  authorizeButton.addEventListener('click', setClientSecretAndClientId);
});