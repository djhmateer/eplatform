function Images() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Images</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <img src="/lake1.jpg" alt="Lake" className="w-full h-48 object-cover rounded mb-2" />
          <p className="text-slate-600 text-center">Lake</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm">
          <img src="/landscape.jpg" alt="Landscape" className="w-full h-48 object-cover rounded mb-2" />
          <p className="text-slate-600 text-center">Landscape</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm">
          <img src="/rainbow.jpg" alt="Rainbow" className="w-full h-48 object-cover rounded mb-2" />
          <p className="text-slate-600 text-center">Rainbow</p>
        </div>
      </div>
    </div>
  )
}

export default Images
