export async function updateDatabase(start: number, stop: number) {
  try {
    const url = `${process.env.UPDATEDB_URL}?start_p=${start}&stop_p=${stop}`;
    if (stop !== null && !isNaN(stop) && stop <= 500) {
      await fetch(url)
        .then((res) => {
          console.log("Success");
        })
        .catch((err) => console.log(err));
    } else {
      alert("Please enter a valid stop value (maximum 500).");
    }
  } catch (err) {
    console.log(err);
  }
}
