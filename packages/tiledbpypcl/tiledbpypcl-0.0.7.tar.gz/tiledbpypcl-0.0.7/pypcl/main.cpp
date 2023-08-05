#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/range_image/range_image.h>
#include <pcl/keypoints/narf_keypoint.h>
#include <pcl/features/range_image_border_extractor.h>
#include <memory>

#include "point_types.hpp"
#include "vector_classes.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;



class CloudFuncs
{
private:
    pcl::PointXYZ* pt;
    pcl::PointCloud<pcl::PointXYZ>* cloud;
public:
    CloudFuncs(float a, float b, float c, int d);

    float add_all_pts();

    bool add_array(std::vector<float> nums);

    int loadXYZCloud(std::vector<float> xs, std::vector<float> ys, std::vector<float> zs);
};

CloudFuncs::CloudFuncs(float a, float b, float c, int d)
{
    cloud = new pcl::PointCloud<pcl::PointXYZ>();
    for (int i = 0; i < d; ++i)
        cloud->push_back({a, b, c});
}

float CloudFuncs::add_all_pts()
{
    float total{0.f};
    for (const auto& pt: *cloud)
        total += (pt.x + pt.y + pt.z);
    return total;
}

bool CloudFuncs::add_array(std::vector<float> nums)
{
    if (nums.size() == 0) return false;
    for (const auto& num: nums)
        if (num != 2.0) return false;
    return true;
}


int CloudFuncs::loadXYZCloud(std::vector<float> xs, std::vector<float> ys, std::vector<float> zs)
{
    if (xs.size() != ys.size() || xs.size() != zs.size())
        return 1;
    size_t size{xs.size()};

    cloud->erase(cloud->begin(), cloud->end());
    for (size_t i = 0; i < size; ++i)
        cloud->push_back({xs[i], ys[i], zs[i]});

    pcl::PointCloud<pcl::PointWithViewpoint> far_ranges;
    Eigen::Affine3f scene_sensor_pose (Eigen::Affine3f::Identity());

    float angular_res{0.5f};
    float support_size{0.2f};
    pcl::RangeImage::CoordinateFrame coordinate_frame = pcl::RangeImage::CAMERA_FRAME;
    bool setUnseenToMaxRange{true};
    float noise_level{0.0f};
    float min_range{0.0f};
    int border_size{1};
    pcl::RangeImage::Ptr range_image_ptr(new pcl::RangeImage);
    const pcl::RangeImage* range_image_raw(range_image_ptr.get());
    pcl::RangeImage& range_image = *range_image_ptr;
    range_image.createFromPointCloud(*cloud, angular_res,
                                     pcl::deg2rad(360.0f), pcl::deg2rad(180.0f),
                                     scene_sensor_pose, coordinate_frame,
                                     noise_level, min_range, border_size);
    range_image.integrateFarRanges(far_ranges);
    if (setUnseenToMaxRange)
        range_image.setUnseenToMaxRange();

    pcl::RangeImageBorderExtractor range_image_border_extractor(range_image_raw);
    pcl::NarfKeypoint narf_Keypoint_detector(&range_image_border_extractor);
    narf_Keypoint_detector.setRangeImage(&range_image);
    narf_Keypoint_detector.getParameters().support_size = support_size;

    pcl::PointCloud<int> keypoint_indices;
    narf_Keypoint_detector.compute(keypoint_indices);

    return keypoint_indices.size();
//    return 0;
}

int add(int i, int j) {
    pcl::PointCloud<pcl::PointXYZ> cloud;
    cloud.push_back({float(i), float(j), float(j)});
    pcl::RangeImage::Ptr range_image_ptr(new pcl::RangeImage);
    return cloud[0].x + cloud[0].y + cloud[0].z;
}
























using PointCloudXYZ = pcl::PointCloud<pcl::PointXYZ>;
using XYZIter = std::__wrap_iter<std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>>::pointer>;



//py::call_guard<py::scoped_ostream_redirect, py::scoped_estream_redirect>()

PYBIND11_MODULE(tiledbpypcl, m) {
    m.doc() = R"pbdoc(
        TileDB: Pybind11 with PCL
        -----------------------

        .. currentmodule:: cmake_example

        .. autosummary::
           :toctree: _generate

            Cloud Funcs
            add
            point types
            PointCloudXYZ

    )pbdoc";

    definePointTypes(m);
    py::module m_vector = m.def_submodule("vectors", "vector types submodule");
    defineVectorClasses(m_vector);

    m.def("add", &add);

    py::class_<CloudFuncs>(m, "CloudFuncs")
        .def(py::init<float, float, float, int>())
        .def("add_all_pts", &CloudFuncs::add_all_pts)
        .def("add_array", &CloudFuncs::add_array)
        .def("loadXYZCloud", &CloudFuncs::loadXYZCloud);

    py::class_<PointCloudXYZ>(m, "PointCloudXYZ")
        .def(py::init<>())
        .def("push_back", &PointCloudXYZ::push_back)
        .def("size", &PointCloudXYZ::size)
//        .def("begin", static_cast<std::vector<pcl::PointXYZ>::iterator (PointCloudXYZ::*)(size_t)>(&PointCloudXYZ::begin));
//        .def("end", &PointCloudXYZ::end)
        .def("at", static_cast<pcl::PointXYZ& (PointCloudXYZ::*)(size_t)>(&PointCloudXYZ::at))
        .def_readonly("points", static_cast<std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>> (PointCloudXYZ::*)>(&PointCloudXYZ::points));

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
