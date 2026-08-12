export default function CommandBar(){
 return (
  <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-[80%] max-w-xl">
   <input
    className="w-full rounded-full bg-black/60 border border-orange-500/40 px-6 py-4 text-white outline-none backdrop-blur"
    placeholder="Type your command..."
   />
  </div>
 );
}
