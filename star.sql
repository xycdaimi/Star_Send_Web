/*
 Navicat Premium Data Transfer

 Source Server         : php
 Source Server Type    : MySQL
 Source Server Version : 80031
 Source Host           : localhost:3306
 Source Schema         : star

 Target Server Type    : MySQL
 Target Server Version : 80031
 File Encoding         : 65001

 Date: 22/06/2024 19:09:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for send
-- ----------------------------
DROP TABLE IF EXISTS `send`;
CREATE TABLE `send`  (
  `订单号` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `寄件人uid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `寄件人姓名` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `寄件人地址` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `寄件人电话` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `寄件人公司` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `收件人uid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `收件人姓名` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `收件人地址` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `收件人电话` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `收件人公司` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `物品类型` int NULL DEFAULT NULL,
  `物品重量` int NULL DEFAULT NULL,
  `物流状态` int NULL DEFAULT 0,
  `派件时间` date NULL DEFAULT NULL,
  `签收时间` date NULL DEFAULT NULL,
  `寄件方式` tinyint NULL DEFAULT NULL,
  `付款方式` tinyint NULL DEFAULT NULL,
  `快递员uid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `快递员电话` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`订单号`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of send
-- ----------------------------
INSERT INTO `send` VALUES ('y3ejacaxbr40000000', 'd9e7veczdaw0000', 'ee', '河北省唐山市路北区sdfjhskjf', '18543142155', 'dsfsfg', 'fu137vsv0bs0000', 'cc', '河北省邯郸市复兴区sdasdas', '18765432111', 'fasfsf', 3, 1, 5, '2023-10-25', '2023-10-25', 2, 2, '56ga0oja9ug0000', '18112234545');
INSERT INTO `send` VALUES ('y80w8ovhkxs0000000', '5se88a13pgw0000', '李四', '河北省邯郸市丛台区dgsfsf', '18454531231', 'sdfsdffs', '3ob85ifvb2q0000', 'luo', '内蒙古自治区乌海市海南区sfadasf', '18065138817', 'asfdaf', 5, 20, 0, NULL, NULL, 2, 3, NULL, NULL);
INSERT INTO `send` VALUES ('1p55lwz2cvwg000000', '3ob85ifvb2q0000', 'luo', '天津市天津市河西区sahjdkahjdf', '18065138817', 'asfsad', '2x88bitb41e0000', 'xyc', '天津市天津市河东区dgsdfsdf', '18065138816', 'dsf', 5, 20, 5, '2023-10-23', '2023-10-25', 2, 2, '1k2yelc2ln40000', '18065138818');
INSERT INTO `send` VALUES ('yoa0wi8hoxs0000000', '3ob85ifvb2q0000', 'luo', '河北省唐山市开平区afasdasd', '18065138817', 'afasdsad', '2x88bitb41e0000', 'xyc', '天津市天津市河东区dgfhfgsg', '18065138816', 'sdfsdfsgd', 2, 3, 4, '2023-10-25', '2024-06-21', 3, 1, '1k2yelc2ln40000', '18065138818');
INSERT INTO `send` VALUES ('t5sp2vujxkw0000000', '17dmaf74md8g000', '张三', '河北省秦皇岛市北戴河区fasdfasf', '18453454512', 'asdasd', '5se88a13pgw0000', '李四', '河北省唐山市路北区ssdfsdfds', '18454531231', 'fsdfsdf', 2, 3, 0, NULL, NULL, 2, 2, NULL, NULL);
INSERT INTO `send` VALUES ('4d7akgpu9wk00000000', '2x88bitb41e0000', 'xyc', '山西省阳泉市矿区lkjaksjdk', '18065138816', 'sfsdaff', '122346s1amy8000', '王五', '安徽省淮南市谢家集区都是风景十分大师傅', '18751231215', '地方撒旦发', 1, 1, 0, NULL, NULL, 1, 1, NULL, NULL);

-- ----------------------------
-- Table structure for usr
-- ----------------------------
DROP TABLE IF EXISTS `usr`;
CREATE TABLE `usr`  (
  `uid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tel` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `kuaidi` tinyint(1) UNSIGNED ZEROFILL NOT NULL,
  `wangdian` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`uid`) USING BTREE,
  INDEX `tel`(`tel`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usr
-- ----------------------------
INSERT INTO `usr` VALUES ('0000', 'admin', 'root', NULL, NULL, NULL, 6, NULL);
INSERT INTO `usr` VALUES ('fu137vsv0bs0000', 'cc', '123', NULL, '18765432111', NULL, 0, NULL);
INSERT INTO `usr` VALUES ('d9e7veczdaw0000', 'ee', '123', NULL, '18543142155', NULL, 5, NULL);
INSERT INTO `usr` VALUES ('9ecba-a9-2a4-a0-', 'tt', '123', NULL, '18065138856', NULL, 0, NULL);
INSERT INTO `usr` VALUES ('122346s1amy8000', '王五', '123', NULL, '18751231215', NULL, 0, NULL);
INSERT INTO `usr` VALUES ('2x88bitb41e0000', 'xyc', '123', NULL, '18065138816', NULL, 2, 'd9e7veczdaw0000');
INSERT INTO `usr` VALUES ('3ob85ifvb2q0000', 'luo', '123', NULL, '18065138817', NULL, 0, NULL);
INSERT INTO `usr` VALUES ('1k2yelc2ln40000', 'bo', '123', NULL, '18065138818', NULL, 2, 'd9e7veczdaw0000');
INSERT INTO `usr` VALUES ('17dmaf74md8g000', '张三', '123', NULL, '18453454512', NULL, 0, NULL);
INSERT INTO `usr` VALUES ('5se88a13pgw0000', '李四', '123', NULL, '18454531231', NULL, 0, NULL);

SET FOREIGN_KEY_CHECKS = 1;
