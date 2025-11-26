const convertTypes = (data) => {
    if (!data) return null;
    return {
        ...data,
        id: Number(data.id),
    }
};

module.exports = {
    convertTypes,
};