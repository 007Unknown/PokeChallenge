let pokemon = document.getElementById("pkm list")
let sidebar = document.getElementById("sidebar")
let load = document.getElementById("load")
let startNumber = 13

function getArg(path, arg) {
    let x = `?name=${arg}`
    if (isNaN(parseInt(arg)) === false){
        x = `?id=${arg}`
    }
    if (path.includes("abilities") || path.includes("types") && (isNaN(parseInt(arg)) === false)){
            x = `?pokemonid=${arg}`
    }
    return x
}

function search(path, arg) {
    let argFinal = getArg(path, arg)
    return fetch(`http://localhost:5000/${path}/${argFinal}`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        })
        .then(res => {
            if(res.ok) {
                return res.json();
            }
            throw new Error('Not successful')
        })
        .then(data => {return data})
        .catch(error => console.error(error))
}

function getInputValue() {
    return document.getElementById("textBox").value;
}

function createPokemon(id) {
    search('pokemon/types', `${id+1}`)
        .then(response => {
            let data = response['data']['0']
            pokemon.innerHTML += `
        <button
            id=${id+1}
	    	class="relative transition duration-200 hover:-translate-y-1
	    	bg-white shadow-lg rounded-[20px] font-bold font-medium
	    	pb-5 py-[55px] px-10 mt-5 mx-4 my-14" onclick="changeSidebar(${id+1})">
	    <div class="sprite absolute -top-6">
	    	<img src="images/sprites/${id+1}.png" alt="${id+1} pokemon">
	    </div>
	    <div class="text-sm pt-2 text-gray-500">
	    	<p>Nº${id+1}</p>
	    </div>
	    <div class="text-black text-lg">
	    	<p id="name-${id+1}">${data['name']}</p>
	    </div>
	    <!-- type(s) -->
	    <div id="types-${id+1}" class="grid grid-cols-2 gap-1">
	    </div>
    </button>
    `
            let pokeTypes = data['types']
            if (pokeTypes.length === 1) {
                document.getElementById(`types-${id+1}`).innerHTML = `
               <div class="rounded-lg bg-slate-300">
                 <div class="col-span-2 text opacity-75 font-bold p-1
                            ${getColor(data['types'][0]['type'])} rounded-lg">
                     ${data['types'][0]['type']}
                 </div>`
            }
            if (pokeTypes.length >= 2) {
                for (let pokeType in pokeTypes){
                    document.getElementById(`types-${id+1}`).innerHTML += `
               <div class="rounded-lg bg-slate-300">
                 <div class="text opacity-75 font-bold p-1
                            ${getColor(data['types'][`${pokeType}`]['type'])} rounded-lg">
                     ${data['types'][`${pokeType}`]['type']}
                 </div>`
                }
            }
        })
}

function changeSidebar(id) {
    search('pokemon', `${id}`)
        .then(response => {
            let data = response[0]
            let total = (data['hp'] + data['attack'] + data['defense'] + data['special_attack'] + data['special_defense'] + data['speed'])
            sidebar.innerHTML = `
    <div class="transition duration-200
             w-[400px] h-[800px]
             text-center bg-white rounded-[20px] shadow-xl">
		<div class="sprite relative -top-[100px] -right-[80px]">
			<img src="images/hd/${id}.png" class="max-w-[200px]" alt="bulbasaur">
		</div>
		<div class="relative -top-[90px]">
			<div class="font-bold text-gray-500">
				<p>#${id}</p>
			</div>
			<div class="text-2xl font-extrabold">
				<p>${data['name']}</p>
			</div>
			<!-- type(s) -->
			<p class="py-1 text-gray-500 text-sm">${data['species']} Pokémon</p>
			<div class="px-4">
				<p class="font-bold py-2 pt-4 uppercase">pokédex entry</p>
				<p>${data['description']}</p>
			</div>
			<div class="grid grid-cols-2 flex justify-center gap-4 mr-5 ml-5 mt-2">
				<p class="col-span-2 font-bold uppercase">Abilities</p>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_AB_NORMAL
				</div>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_AB_HIDDEN
				</div>
				<p class="font-bold uppercase">height</p>
				<p class="font-bold uppercase">weight</p>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					${data['height']} m
				</div>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					${data['weight']} kg
				</div>
				<p class="font-bold uppercase">weaknesses</p>
				<p class="font-bold uppercase">base exp</p>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_WEAKNESS
				</div>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					${data['base_experience']}
				</div>
			</div>
			<p class="font-bold uppercase py-2">Stats</p>
			<div class="flex items-center
						text text-center
						grid grid-cols-7 px-5 gap-4">
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-red-400 uppercase">hp</p>
					<p class="static rounded-[20px] ">${data['hp']}</p>
				</div>
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-orange-400 uppercase">atk</p>
					<p class="static rounded-[20px]">${data['attack']}</p>
				</div>
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-yellow-400 uppercase">def</p>
					<p class="static rounded-[20px] ">${data['defense']}</p>
				</div>
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-sky-400">SpA</p>
					<p class="static rounded-[20px] ">${data['special_attack']}</p>
				</div>
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-green-400">SpD</p>
					<p class="static rounded-[20px] ">${data['special_defense']}</p>
				</div>
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-pink-400 uppercase">spd</p>
					<p class="static rounded-[20px] ">${data['speed']}</p>
				</div>
				<div class="bg-slate-200 rounded-[20px] p-1">
					<p class="rounded-[20px] p-1 bg-blue-400 uppercase">tot</p>
					<p class="static rounded-[20px] ">${total}</p>
				</div>
			</div>
			<div class="py-5">
				<div class="py-4 m-2 rounded-[20px] grid grid-cols-2 gap-2 bg-slate-200 shadow-md">
					<div class="previous hover:bg-gray-300 rounded-[20px] ">
						<i class="absolute left-5 material-icons text-sm scale-150 pr-1">arrow_back_ios</i>
						TID_PREVIOUS_${id-1}
					</div>
					<div class="next hover:bg-gray-300 rounded-[20px]">
						TID_NEXT_${id+1}
						<i class="absolute right-5 material-icons text-sm scale-150">arrow_forward_ios</i>
					</div>
				</div>
			</div>
		</div>
	</div>
    `
        })
}

function changePkmList() {
    search('pokemon/types', getInputValue())
        .then(response => {
            let data = response['data']['0']
            let pid = data['id']
            pokemon.innerHTML = ``
            createPokemon(pid-1)
            load.innerHTML = `
            <div class="hidden"></div>`
        }
    )
}


async function createMany(start, end) {
    for (let i = start-1; i < end; i++){
        createPokemon(i)
        await sleep(100)
    }
}

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

function getColor(type) {
    switch(type){
        case 'Normal':
            return 'bg-gray-300'
        case 'Bug':
            return 'bg-lime-600'
        case 'Dark':
            return 'bg-zinc-700'
        case 'Dragon':
            return 'bg-blue-600'
        case 'Electric':
            return 'bg-yellow-400'
        case 'Fairy':
            return 'bg-pink-500'
        case 'Fighting':
            return 'bg-rose-600'
        case 'Fire':
            return 'bg-red-600'
        case 'Flying':
            return 'bg-teal-200'
        case 'Ghost':
            return 'bg-purple-800'
        case 'Grass':
            return 'bg-green-500'
        case 'Ground':
            return 'bg-amber-700'
        case 'Ice':
            return 'bg-cyan-400'
        case 'Poison':
            return 'bg-purple-400'
        case 'Psychic':
            return 'bg-violet-600'
        case 'Rock':
            return 'bg-amber-800'
        case 'Steel':
            return 'bg-zinc-500'
        case 'Water':
            return 'bg-sky-500'
    }
}

function createLoadMore(start, end) {
    createMany(start, end).then()
    startNumber += 6
}

// arbitrary numbers for testing
createMany(1, 16).then()
