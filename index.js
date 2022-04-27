import PetMap from '@/components/PetMap';

const components = {
    PetMap,
}

const install = function (Vue, Option) {
    Object.keys(components).forEach((key) => {
       Vue.component(components[key].name, components[key])
   })
}

export default {
   install
}