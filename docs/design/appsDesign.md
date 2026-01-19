There are 3 apps that should exist in this project.  Ores which list the base materials that all components are made from, components which list all parts that can be used to build blocks, and blocks which list all blocks.

Each app should have the following models:
- object_id - A unique identifier for each object. datatype: uuid7 (required, primary key)
- name - The name of the object. datatype: string (required, unique)
- description - A brief description of the object. datatype: string
- mass - The mass of the object in kilograms. datatype: float (required)
- created_at - Timestamp of when the object was created. datatype: datetime, auto-set on creation utcnow (required)
- updated_at - Timestamp of when the object was last updated. datatype: datetime, auto-set on update utcnow (required) 

Unique requirements for each app:
Ores:

Components:
- material - list of foreign keys to the ore that the component is made from and quantities. Can have multiple ore types. datatype: JSONField
- fabricator - The machine that is used to create the component string. datatype: string
- crafting_time - The time it takes to craft the component in seconds datatype: float

Blocks:
- components - list of foreign keys to the components that make up the block and quantities. Can have multiple component types. datatype: JSONField
- health - The health of the block. datatype: float
- pcu - The PCU (Performance Cost Unit) of the block. datatype: integer
- snap_size - The snap size of the block. datatype: float
- input_mass - The input mass capacity of the block. datatype: integer
- output_mass - The output mass capacity of the block. datatype: integer
- consumer_type: The type of consumer (e.g., power, oxygen). datatype: string (optional)
- consumer_rate: The rate at which the block consumes resources. datatype: float (0 if no consumer_type)
- producer_type: The type of producer (e.g., power, oxygen). datatype: string (optional)
- producer_rate: The rate at which the block produces resources. datatype: float (0 if no producer_type)
- storace_capacity - The storage capacity of the block. datatype: float (optional)

Each app should have the following views:
- ListView - A view to list all objects in the app and the ability to filter by name and sort by mass.
- DetailView - A view to see the details of a specific object.
- CreateView - A view to create a new object.
- UpdateView - A view to update an existing object.
- DeleteView - A view to delete an existing object.

There should be a view that allows users to select multiple blocks with quantities and add them to a build order.  The build order should calculate the total mass, tell the components, fabricators, crafting times, and ores required to complete the build order.
